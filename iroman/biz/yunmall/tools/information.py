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
        for i in range(settings.RETRY_COUNT):
            page = self.request.get(settings.INFORMATION_URL)
            LOG.info("Get member/information.html return: %s", page.status_code)
            if not page.ok:
                time.sleep(i+1)
            else:
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

    def _info(self, invate_code, mobile, sms_code, img_code):
        username, pwd = utils.gen_username(), settings.DEFAULT_PWD
        payload = {
            "u[password]": pwd,
            "u[repeat_password]": pwd,
            "u[phone]": mobile,
            "u[protocol]": "on",
            "u[smsCode]": sms_code,
            "u[veryCode]": img_code,
            "u[re_phone]": None,
            "u[re_user_id]": None,
            "u[username]": username,
        }
        header = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        resp = self.request.post(settings.REGISTER_POST_URL, data=payload,
                                headers=header)
        LOG.info("register submit payloaa: %s", payload)
        result = False
        if resp.ok:
            ret = resp.json()
            LOG.info("register submit return is: %s",
                        REGISTER_CODE.DISPLAY.get(ret, ret))
            
            if ret == REGISTER_CODE.SUCCEED:
                result = True
                Fish.new(invate_code, username, pwd, mobile)

            if ret == REGISTER_CODE.FAILED:
                pass 
        else:
            LOG.info("register submit status_code: %s", resp.status_code)

        return result

    def _save_invate_code(self, content):
        soup = BeautifulSoup(content, "lxml")
        #print soup.prettify()
        member = soup.find("td", attrs={"class", "member-info-cols-w"})
        LOG.info("basic info page find member element: %s", member)
        if member:
            member_id = member.find_next_sibling("td")
            if member_id:
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
        LOG.debug("submit basic info resp.content: %s", resp.content)
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
                return True
                
        return False


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
        LOG.info("set paypassword port url: %s", pay_url)
        resp = self.request.post(pay_url, data=payload,
                                headers=header)
        LOG.debug("submit payment info resp.content: %s", resp.content)
        if resp.ok:
            ret = resp.json()
            LOG.info("submit payment info return is: %s",
                        PAY_INFO_RESULT.DISPLAY.get(ret, ret)) 

            if ret == PAY_INFO_RESULT.OK:
                self.fresher.pay_password = "663366"
                self.fresher.step = 3;
                self.fresher.save()
                return True
                
        return False


        
    def start(self):
        if not self.fresher:
            LOG.info("No person need to submit information, exit.")
            return False
        result = False 
        page = self._open_basic_info_page() 
        content = page.content 
        self._save_invate_code(content)
       
        try:
            for i in range(settings.RETRY_COUNT): 
                if self._submit_basic_info():
                    break
        except Exception as ex:
            LOG.exception("submit basic info raise exception.")

        try:
            for i in range(settings.RETRY_COUNT): 
                time.sleep(2)
                page = self._open_set_payment_page() 
                cracked, very_code = self._crack_verify_img()
                if self._submit_payment_info(page.content, very_code):
                    result = True
                    break
        except Exception as ex:
            LOG.exception("submit payment info raise exception.")

        return result
