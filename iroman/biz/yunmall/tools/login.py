#-*- coding=utf-8 -*-

from bs4 import BeautifulSoup
import logging
import os
import requests
import random
import re
import shutil
import string
from selenium import webdriver
import time
import urllib

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from common import utils
from common.utils import DAMA_API as DAMA
from common.utils import MOBILE_API as MOBILE

from biz.yunmall.models import (Fish, ExcceedCode, ExcceedMobile, Config)
from biz.yunmall.tools.information import YunmallInfo
from biz.yunmall.settings import (VERIFY_CODE, SMS_SEND_CODE, REGISTER_CODE,
                                CONFIG, BASIC_INFO_RESULT, PAY_INFO_RESULT)

LOG = logging.getLogger(__name__)


class SeleniumLogin():
    def __init__(self, fresher):
        self.fresher = fresher
        self.PHPSESSID = None

    def get_login_session(self):
        def _loop_login():
            LOG.info("selenium try login: %s", self.browser.current_url)
            phone = self.browser.find_element_by_id("phone")
            phone.clear()
            phone.send_keys(self.fresher.mobile)

            pwd = self.browser.find_element_by_id("password")
            pwd.clear()
            pwd.send_keys(self.fresher.password)

            login_type = self.browser.find_elements_by_name("u[loginType]")
            for radio in login_type:
                if radio.get_attribute("value") == "phone":
                    radio.click()

            login_button = self.browser.find_element_by_id("login-btn")
            login_button.click()

            time.sleep(2)
            LOG.info("selenium login result: %s", self.browser.current_url)
            return self.browser.current_url.find("/login/index.html") < 0

        self.browser.get(settings.LOGIN_GET_URL)
        logined = _loop_login()
        index = 0
        while not logined:
            logined = _loop_login()
            if logined:
                break

            index = index + 1

            if index > settings.RETRY_COUNT:
                break

        if logined:
            self.PHPSESSID = self.browser.get_cookie("PHPSESSID")\
                                    .get("value", None)

    def __enter__(self):
        self.browser = webdriver.Firefox()
        return self

    def __exit__(self, type, value, traceback):
        try:
            time.sleep(2)
            self.browser.quit()
        except Exception as ex:
            LOG.exception("selenium quit browser raise exception.")


class YunmallLogin():
    def __init__(self, fresher, session=None): 
        self.request = requests.Session()
        header = settings.HTTP_HEADER.copy()
        header["Cookie"] = session
        header["Referer"] = settings.MEMBER_INDEX_URL
        self.request.headers.update(header)
        self.fresher = fresher

    def start(self):
        result = False 
        if not self.fresher:
            LOG.info("No person need to submit information, exit.")
            return result  

        # login succeed, submit information 
        for i in range(settings.RETRY_COUNT):
            try:
                info = YunmallInfo(self.request, self.fresher)
                if info.start():
                    result = True
                    break
            except Exception as ex:
                LOG.error(ex.message)
                time.sleep(2)
        return result
