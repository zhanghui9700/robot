#-*- coding=utf-8 -*-

from bs4 import BeautifulSoup
import logging
import os
import requests
import random
import re
import shutil
import string
import time

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from common import utils
from common.utils import DAMA_API as DAMA
from common.utils import MOBILE_API as MOBILE

from biz.yunmall.models import (Fish, ExcceedCode, ExcceedMobile, Config)
from biz.yunmall.settings import (VERIFY_CODE, SMS_SEND_CODE, REGISTER_CODE,
                                CONFIG, BASIC_INFO_RESULT, PAY_INFO_RESULT)

LOG = logging.getLogger(__name__)
INFO, PAY = 1, 2


class YunmallInfo():
    def __init__(self, request, fresher):
        self.request = request
        self.fresher = fresher

    def _save_img(self, url):
        seed = str(random.random())
        img = self.request.get(settings.VERIFY_IMAGE_URL + "?t=" + seed,
                          stream=True)
        path = None
        if img.ok:
            path = settings.VERIFY_IMAGE_REPO % seed
            with open(path, "wb") as f:
                img.raw.decode_content = True
                shutil.copyfileobj(img.raw, f)

        return path

    def _crack_verify_img(self):
        img_path = None
        for i in range(settings.RETRY_COUNT):
            img_path = self._save_img(settings.VERIFY_IMAGE_URL)
            if not img_path:
                time.sleep(i+1)
            else:
                break

        if not img_path:
            raise Exception("veify image download failed.")
        
        cracked, code = False, None
        for i in range(settings.RETRY_COUNT): 
            cracked, code = DAMA.decode(img_path, settings.DM2_IMG_TYPE)
            LOG.info("save verify image to: %s, cracked: %s, code: %s",
                                    img_path, cracked, code)
            if cracked:
                break

        os.remove(img_path)

        if not cracked:
            raise Exception("dama api crack image failed.")

        return cracked, code 

    def _open_basic_info_page(self):
        page = None
        i = 0
        while True:
            page = self.request.get(settings.INFORMATION_URL)
            LOG.info("Get member/information.html, result: %s %s", 
                            page.url, page.status_code)
            if page.ok and page.url.find("/member/information.html") >= 0:
                break
            else:
                i = i + 1
                time.sleep(3)

            if i > 20:
                break

        if not page or not page.ok: 
            raise Exception("Open information page failed.")

        return page

    def _check_verify_img(self, img_code):
        payload = {"v": img_code} 
        result = False
        for i in range(3):
            resp = self.request.post(settings.VERIFY_IMAGE_CHECK_URL, data=payload)
            if resp.ok:
                ret = resp.json() 
                LOG.debug("check veify image return: %s",
                            VERIFY_CODE.DISPLAY.get(ret, ret))
                if ret == VERIFY_CODE.OK:
                    result = True
                    break
                if ret == VERIFY_CODE.FAILED:
                    pass

        return result

    def _save_invate_code(self, content):
        soup = BeautifulSoup(content, "lxml")
        #print soup.prettify()
        member = soup.find("td", attrs={"class", "member-info-cols-w"})
        LOG.info("basic info page find member element: %s", member)
        if member:
            member_id = member.find_next_sibling("td")
            if member_id:
                LOG.info("basic info page find self invate_code: %s",
                                member_id.string)
                self.fresher.code = member_id.string
                self.fresher.save()

        if not self.fresher.code:
            raise Exception("save self invate code failed.")

    def _submit_basic_info(self): 
        email, id_card, nick_name, new_password = utils.gen_basic_info()
        payload = {
            "u[email]": email,   
            "u[identity_card_num]": id_card,
            "u[nickname]": nick_name,
            "u[oldPassword]": self.fresher.password,
            "u[password]": new_password,
            "u[username]": self.fresher.username,
        }

        header = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        result = False

        resp = self.request.post(settings.INFORMATION_URL+"?t=1", data=payload,
                            headers=header)

        if resp.url.find("/member/information.html") < 0:
            LOG.debug("submit basic info post resp.url: %s", resp.url)
            return result

        if resp.ok:
            ret = resp.json()
            LOG.info("submit basic info return is: %s",
                        BASIC_INFO_RESULT.DISPLAY.get(ret, ret)) 

            if ret == BASIC_INFO_RESULT.OK:
                self.fresher.email = email
                self.fresher.id_card = id_card
                self.fresher.nickname = nick_name
                self.fresher.password = new_password
                self.fresher.step = 2
                self.fresher.save()
                result = True
        else:
            LOG.debug("submit basic info resp.content: %s", resp.content)
                
        return result


    def _open_set_payment_page(self):
        page = None
        for i in range(settings.RETRY_COUNT):
            page = self.request.get(settings.SET_PAYMENT_URL)
            LOG.info("Get member/paypassword.html return: %s", page.status_code)
            if not page.ok:
                time.sleep(i+1)
            else:
                break

        if not page or not page.ok: 
            raise Exception("Open paypassword page failed.")

        return page 

    def _submit_payment_info(self, content, very_code):
        #soup = BeautifulSoup(content, "lxml")
        #member = soup.find("td", attrs={"class", "member-info-cols-w"})
   
        payload = {
            "u[oldPassword]": self.fresher.password, 
            "u[payPassword]": "663366", 
            "u[phone]": self.fresher.mobile,   
            "u[veryCode]": very_code,
        }
        header = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        result = False
        start = content.find("$.post('/member/setPayPassword")
        if start < 0:
            raise Exception("Set payment password page content incorrect.")

        end = content.find(",", start)
        pay_url = "%s%s" % (settings.YUNMALL_HOST, content[start+8: end-1])

        for i in range(settings.RETRY_COUNT):
            resp = self.request.post(pay_url, data=payload,
                                    headers=header)
            
            LOG.debug("set paypassword port url: %s, resp.url: %s", pay_url,
                                                                resp.url)
            if resp.url.find("/member/index") >= 0:
                break

            #LOG.debug("submit payment info resp.content: %s", resp.content)
            if resp.ok:
                ret = resp.json()
                LOG.info("submit payment info return is: %s",
                            PAY_INFO_RESULT.DISPLAY.get(ret, ret)) 

                if ret == PAY_INFO_RESULT.OK:
                    self.fresher.pay_password = "663366"
                    self.fresher.step = 3;
                    self.fresher.save()
                    result = True
                    break 
                
        return result

    def _open_index_page(self):
        page = self.request.get(settings.MEMBER_INDEX_URL)
        LOG.info("Get member/index.html, result: %s %s", 
                            page.url, page.status_code)
        jump = None
        if page.ok:
            content = page.content 
            info = content.find("'location.href = \"/member/information.html\"'")
            pay = content.find("'location.href = \"/member/payPassword.html\"")
            LOG.info("index page find INFO=%s, PAY=%s", info, pay)
            if info >= 0:
                jump = INFO

            if pay >= 0:
                jump = PAY

        return jump

        
    def start(self):
        if not self.fresher:
            LOG.info("No person need to submit information, exit.")
            return False
        result = False 
        
        self._open_index_page()

        jump = INFO   
        index = 0
        while jump:
            time.sleep(3)
            if jump == INFO:
                try:
                    page = self._open_basic_info_page() 
                    content = page.content 
                    self._save_invate_code(content)
                    if self._submit_basic_info():
                        LOG.info("----------submit basic info OK-------------")
                except Exception as ex:
                    LOG.exception("submit basic info raise exception.")

            if jump == PAY:
                try:
                    page = self._open_set_payment_page() 
                    cracked, very_code = self._crack_verify_img()
                    if self._submit_payment_info(page.content, very_code):
                        LOG.info("==========submit payment info OK==========")
                except Exception as ex:
                    time.sleep(5)
                    LOG.exception("submit payment info raise exception.")

            jump = self._open_index_page()

            if not jump:
                result = True
                break

            index = index + 1
            if index > 20:
                break

        return result
