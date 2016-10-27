#-*- coding=utf-8-*-

import logging
import requests
import random
import shutil

from django.conf import settings

from common.utils import DAMA_API as DAMA
from common.utils import MOBILE_API as MOBILE

from .models import (Fish, ExcceedCode)
from .settings import VERIFY_CODE, SMS_SEND_CODE

LOG = logging.getLogger(__name__)


class Yunmall():

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
        code = None
        for i in range(10):
            code = MOBILE.get_verify_code(mobile)
            if not code:
                time.sleep(5)
            else:
                break

    def _send_sms_code(self, img_code, mobile):
       	payload = {
            "phone": mobile,
            "smsType": "webRegister",
            "veryCode": img_code
	    }
        resp = self.request.post(settings.SEND_SMS_URL, data=payload)
        if resp.ok:
            ret = resp.json();
            LOG.info("send sms code return: %s", ret)
            # TODO: error code
            if ret == SMS_SEND_CODE["OK"]:
                return True
            if ret == SMS_SEND_CODE["EXIST"]:
                LOG.info("Mobile %s already exist, add to black.", mobile)
                MOBILE.add_to_black(mobile) 

        return False
        
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
        resp = self.request.post(settings.VERIFY_IMAGE_CHECK_URL, data=payload)
        if resp.ok:
            ret = resp.json() 
            LOG.info("check veify image return: %s", ret)
            # TODO: error code
            if ret == VERIFY_CODE["OK"]:
                return True
            else:
                return False

    def _register(self):
        payload = {}
        self.request.post()

    def _check_day_quota(self):
        # TODO: day quota check
        pass

    def _check_paused(self):
        # TODO: paused by admin
        pass
    
    def start(self): 
        self._check_paused()
        self._check_day_quota()
        self._open_register_page() 

        try:
            self.code = self._check_invate_code(code=self.code)
        except Exception as ex:
            LOG.error(ex.message)

        if not self.code:
            self.code = self._find_invate_code()

        if not self.code:
            LOG.error("Get invate code failed, exist.")
            return

        LOG.info("Try regisete, invate code: %s", self.code)

        try:
            cracked, img_value = self._crack_verify_img()
        except Exception as ex:
            LOG.exception("crack verify image failed, exit.")
            return

        if not self._check_verify_img(img_value):
            LOG.error("check verify image failed, exit.")
            return

        try:
            mobiles = self._get_mobiles()
        except Exception as ex:
            LOG.error("get mobiles failed, exit.")
            return
        
        while mobiles:
            mobile = mobiles.pop() 
            if self._send_sms_code(img_value, mobile):
                code = self._get_sms_code(mobile)
                LOG.info("get sms code is %s", code)
                # TODO: register
                #self._register()

        print "end..."
