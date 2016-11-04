# -*- coding=utf-8 -*-

import logging
import requests

from django.conf import settings

LOG = logging.getLogger(__name__)


class TMApi():

    def __init__(self, user, pwd, pid):
        self.user = user
        self.pwd = pwd
        self.pid = pid
        self.request = requests.Session()
        self.token = None

    @property
    def logined(self):
        return bool(self.token)

    def _check_login(self): 
        if not self.logined:
            self._login()

        if not self.logined:
            raise Exception("Yma not login")

    def _convert2utf8(self, content):
        if type(content) == str:
            content = content.decode("gb2312")
        return content

    def _get(self, url, payload):
        if not payload.has_key("code"):
            payload["code"] = "utf8"
        resp = self.request.get(url, params=payload)
        if resp.ok:
            #LOG.info("Yma request succeed, payload=%s content=%s",
            #        payload, resp.content)
            pass
        else:
            LOG.error("Yma request failed, payload=%s", payload)

        return resp
 
    def _login(self): 
        """
        http://www.tianma168.com:10001/tm/Login?uName=用户名&pWord=密码&Developer=开发者
        登录token&账户余额&最大登录客户端个数&最多获取号码数&单个客户端最多获取号码数&折扣
        """
        self.token = None
        payload = {
            "uName": self.user,
            "pWord": self.pwd,
        }
        login_url = "%s%s" % (settings.TM_HOST, "Login")
        resp = self._get(login_url, payload=payload)
        if resp.ok:
            content = self._convert2utf8(resp.content)
            result  = content.split('&')
            LOG.info("Tianma login api return: %s", result)
            if len(result) != 2 and result[0].lower() != "false":
                self.token = result[0]

        if not self.token: 
            raise Exception("TianMa login error. params=%s", payload)

    def get_mobiles(self, size=1):
        """
        http://www.tianma168.com:10001/tm/getPhone?ItemId=项目ID&token=登陆token
        正确返回：13112345678;13698763743;13928370932;
        接口如有错误,或者没有获取到号码，前端都会有一个False:后面则是错误信息
        """
        self._check_login()
        size = 10 if size > 10 else size
        payload = {
            "token": self.token,
            "ItemId": self.pid,
            "Count": size,
        }
        get_url = "%s%s" % (settings.TM_HOST, "getPhone")
        resp = self._get(get_url, payload=payload) 
        mobiles = []
        if resp.ok:
            content = self._convert2utf8(resp.content)
            LOG.info("Tianma get mobiles response content: %s", content)

            content = content.lower()
            if not content.startswith("false"):
                mobiles = content.split(';') 
    
        mobiles = [m for m in mobiles if len(m) > 0]

        return mobiles

    def get_verify_code(self, mobile=None):
        """
        http://www.tianma168.com:10001/tm/getMessage?token=登陆token&itemId=项目ID&phone=手机号码
        正确返回：
            1. 短信内容划分都已 & 符号分割
            2. False:没有短信，请5秒后再试
            3. 短信内容:MSG&短信内容
            3. 发送状态:STATE&状态信息
            4. 号码释放通知:RES&项目ID&号码
            5. 接口如有错误,或者没有获取到短信，前端都会有一个False:后面则是错误信息
        """
        if not mobile:
            raise Exception("Tianma get verify code mobile is None.")

        self._check_login()
        payload = {
            "token": self.token,
            "itemid": self.pid,
            "phone": mobile,
        }
        code = None
        get_url =  "%s%s" % (settings.TM_HOST, "getMessage")
        resp = self._get(get_url, payload=payload)       
        if resp.ok:
            content = self._convert2utf8(resp.content)
            LOG.info("Tianma get verify code: %s", content)
            content = content.lower()
            if content.startswith("msg"):
                msg, code = content.split('&')

        return code
        
    def add_to_black(self, mobile=None):
        """
        http://www.tianma168.com:10001/tm/addBlack?token=登陆token&phoneList=itemId-phone
        正确返回:OK  
        注意：当加入黑名单的号码系统会自动释放此号码.
        以下两种情况务必加黑不然后期依然会获取到此号码:
        1.获取的号码不能使用或已注册.   2.获取的号码收不到短信
        """
        if not mobile:
            return

        self._check_login()
        
        payload = {
            "action": "addIgnoreList",
            "phoneList": "%s-%s" % (self.pid, mobile),
        }
        get_url = "%s%s" % (settings.TM_HOST, "addBlack")
        resp = self._get(get_url, payload=payload)       
        if resp.ok:
            content = self._convert2utf8(resp.content)
            LOG.debug("Tianma add %s to black return: %s", mobile, content) 
            

if __name__ == "__main__":
    api = TMApi(settings.TM_USER,
                settings.TM_USER_PWD,
                settings.TM_PID)
    api.get_mobiles(settings.TM_BATCH_MOBILE)

    """
    while True:
        import time
        time.sleep(5)
        api.get_verify_code("17186426278")
    """


API = TMApi(settings.TM_USER, settings.TM_USER_PWD, settings.TM_PID)
