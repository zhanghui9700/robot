#-*- coding=utf-8 -*-

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
                                CONFIG)
from biz.yunmall.tools.information import YunmallInfo

LOG = logging.getLogger(__name__)


class YunmallRegister():

    def __init__(self, code=None):
        self.request = requests.Session()
        self.request.headers.update(settings.HTTP_HEADER)
        self.code = code

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

    def _open_register_page(self):
        for i in range(settings.RETRY_COUNT):
            page = self.request.get(settings.REGISTER_URL)
            LOG.info("Get register.html return: %s", page.status_code)
            if not page.ok:
                time.sleep(i+1)
            else:
                break

        if not page.ok: 
            raise Exception("Register failed open register page error.")

        return page

    def _get_mobiles(self):
        mobiles = None
        for i in range(settings.RETRY_COUNT):
            mobiles = MOBILE.get_mobiles(settings.YMA_BATCH_MOBILE)
            if not mobiles:
                time.sleep(5)
            else:
                break 

        if not mobiles:
            raise Exception("Get yma mobiles failed.")

        return mobiles

    def _get_sms_code(self, mobile=None):
        if not mobile:
            return None

        code, sms = None, None
        for i in range(10):
            sms  = MOBILE.get_verify_code(mobile)
            if not sms:
                time.sleep(5)
            else:
                break
        
        if sms:
            m = re.search(settings.SMS_CODE_PATTERN, sms)
            if m:
                code = m.group()

        LOG.info("get sms code is %s", sms)
        return code

    def _send_sms_code(self, img_code, mobile):
        result = False
       	payload = {
            "phone": mobile,
            "smsType": "webRegister",
            "veryCode": img_code
	    }
        for i in range(2):
            time.sleep(i+1)
            resp = self.request.post(settings.SEND_SMS_URL, data=payload)
            if resp.ok:
                ret = resp.json();
                LOG.info("send %s sms code return: %s", mobile,
                            SMS_SEND_CODE.DISPLAY.get(ret, ret))

                if ret == SMS_SEND_CODE.OK:
                    result = True
                    break

                if ret == SMS_SEND_CODE.FREQUENCY:
                    time.sleep(10)

                if ret == SMS_SEND_CODE.REGISTED:
                    LOG.info("Mobile %s already exist, add to black.", mobile)
                    ExcceedMobile.record(mobile=mobile) 
                    #MOBILE.add_to_black(mobile) 
                    break

                if ret == SMS_SEND_CODE.IMAGE_ERROR:
                    time.sleep(1)

        return result
        
    def _check_invate_code(self, code=None):
        if not code:
           return None

        if ExcceedCode.exist(code=code):
            msg = "Quota excceed in db, code=%s" % code
            self.code = None
            LOG.info(msg)
            return None
            
        payload = {
            'reUserId': code,
            'type': 'phone'
        }
        resp = self.request.post(settings.CHECK_INVATE_URL,
                                data=payload)
        if resp.ok:
            ret = resp.json()
            if ret in ["202", 202]:
                Fish.mark_excceed(code=code)
                msg = "Quota excceed, code=%s" % code
                self.code = None
                raise Exception(msg)
            if ret in ["36", 36]:
                msg = "Invate not exist, code=%s" % code
                self.code = None
                raise Exception(msg)
            
            return code
        else:
            raise Exception("Invate code quota check failed.")
    
    def _find_invate_code(self):
        code = None
        for i in range(settings.RETRY_COUNT):
            invator = Fish.get_invator()
            if invator:
                try:
                    code = self._check_invate_code(code=invator.code) 
                except Exception as ex:
                    time.sleep(i+1)
                if code:
                    break

        return code

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

    def _register(self, invate_code, mobile, sms_code, img_code):
        username, pwd = utils.gen_username(), settings.DEFAULT_PWD
        payload = {
            "u[password]": pwd,
            "u[repeat_password]": pwd,
            "u[phone]": mobile,
            "u[protocol]": "on",
            "u[smsCode]": sms_code,
            "u[veryCode]": img_code,
            "u[re_phone]": invate_code,
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
                result = Fish.new(invate_code, username, pwd, mobile)
                MOBILE.add_to_black(mobile) 

            if ret == REGISTER_CODE.FAILED:
                pass 
        else:
            LOG.info("register submit status_code: %s", resp.status_code)

        return result

    def _check_day_quota(self):
        conf = Config.get_conf(CONFIG.DAY_QUOTA)
        if conf and conf.value and conf.value.isdigit():
            quota = int(conf.value)
            today = Fish.today_reg_count()
            result =  today >= quota
            LOG.debug("System day quota %s, today: %s.", quota, today)
            return result
        return False

    def _check_paused(self):
        conf = Config.get_conf(CONFIG.PAUSED)
        if conf and conf.value:
            LOG.debug("System paused value is: %s.", conf.value)
            return utils.bool_from_string(conf.value)
        return False

    def _get_invate_code(self):
        # invate code
        try:
            self.code = self._check_invate_code(code=self.code)
        except Exception as ex:
            LOG.error(ex.message)

        if not self.code:
            self.code = self._find_invate_code()
 
    def start(self):
        if self._check_paused():
            LOG.info("System exit by paused.")
            return

        if self._check_day_quota():
            LOG.info("System exit by day quota excceed.")
            return

        result = False 

        self._open_register_page() 
        self._get_invate_code()

        if not self.code:
            LOG.error("Get invate code failed, exist.")
            return
        
        LOG.info("Try regisete, invate code: %s", self.code)

        # image verify code
        try:
            cracked, img_value = self._crack_verify_img()
        except Exception as ex:
            LOG.exception("crack verify image failed, exit.")
            return

        if not self._check_verify_img(img_value):
            LOG.error("check verify image failed, exit.")
            return

        # mobile
        try:
            mobiles = self._get_mobiles()
        except Exception as ex:
            LOG.error("get mobiles failed, exit.")
            return
        
        # sms code
        sms_code = None
        while mobiles:
            mobile = mobiles.pop() 

            if ExcceedMobile.exist(mobile):
                continue

            if self._send_sms_code(img_value, mobile):
                sms_code = self._get_sms_code(mobile)
                if sms_code:
                    break

        # register submit
        fresher = None
        if sms_code:
            fresher = self._register(self.code, mobile, sms_code, img_value)
        
        # register succeed, submit information 
        if fresher:
            for i in range(settings.RETRY_COUNT):
                try:
                    info = YunmallInfo(self.request, fresher)
                    if info.start():
                        result =True
                        break
                except:
                    time.sleep(2)

        return result
