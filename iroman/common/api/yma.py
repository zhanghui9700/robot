# -*- coding=utf-8 -*-

import logging
import requests

from django.conf import settings

LOG = logging.getLogger(__name__)


class YmaApi():

    def __init__(self, user, pwd, pid):
        self.user = user
        self.pwd = pwd
        self.pid = pid
        self.request = requests.Session()
        self.token = None

        self.login()

    @property
    def logined(self):
        return bool(self.token)

    def _get(self, url, payload):
        resp = self.request.get(url, params=payload)
        if resp.ok:
            #LOG.info("Yma request succeed, payload=%s content=%s",
            #        payload, resp.content)
            pass
        else:
            LOG.error("Yma request failed, payload=%s", payload)

        return resp
 
    def login(self): 
        self.token = None
        payload = {
            "action": "loginIn",
            "uid": self.user,
            "pwd": self.pwd,
        }
        resp = self._get(settings.YMA_HOST, payload=payload)
        if resp.ok:
            content = resp.content.split('|')
            if len(content) == 2 and content[0] == self.user:
                self.token = content[1]

        if not self.token: 
            raise Exception("Yma login error. params=", payload)

    def get_mobiles(self, size=1):
        """
        http://www.yma0.com/list.aspx?cid=2#mj21
        no_data 系统暂时没有可用号码了
        max_count_disable   已达到用户可获取号码上限，可通过调用ReleaseMobile方法释放号码并终止任务
        parameter_error 传入参数错误
        not_login   没有登录,在没有登录下去访问需要登录的资源，忘记传入uid,token
        message|please try again later  访问速度过快，建议休眠50毫秒后再试
        account_is_locked   账号被锁定
        mobile_notexists    指定的号码不存在
        mobile_busy 指定的号码繁忙
        unknow_error    未知错误,再次请求就会正确返回
        """
        if not self.logined:
            self.login()

        if not self.logined:
            raise Exception("Yma not login")

        size = 10 if size > 10 else size
 
        payload = {
            "action": "getMobilenum",
            "token": self.token,
            "pid": self.pid,
            "uid": self.user,
            "size": size,
        }
        resp = self._get(settings.YMA_HOST, payload=payload)       
        if resp.ok:
            # 18508328761;17070273426;15999897314|2856f43fdee5c7fa
            content = resp.content
            LOG.info("Yma get mobiles response content: %s", content)
            if resp.content.rfind("|") > 0:
                content = resp.content.split('|')
                if len(content) == 2 and content[1] == self.token:
                    mobiles = content[0].split(";")
                    return mobiles
                else:
                    LOG.error("Yma get mobiles resp.content format error, "
                           "content=%s", content)

        return None

    def get_verify_code(self, mobile=None):
        """
        response.content
        17186426278|[发送号码：10690222357]【匀加速商城】尊敬的用户，您的验证码为130519，本验证码10分钟内有效，感谢您的使用。
        """
        if not mobile:
            raise Exception("Yma get verify code mobile is None.")

        if not self.logined:
            self.login()

        if not self.logined:
            raise Exception("Yma not login")

        payload = {
            "action": "getVcodeAndHoldMobilenum",
            "token": self.token,
            "pid": self.pid,
            "uid": self.user,
            "mobile": mobile,
        }
        code = None
        resp = self._get(settings.YMA_HOST, payload=payload)       
        if resp.ok:
            content = resp.content
            LOG.info("Yma get verify code: %s", content)
            if resp.content.rfind("|") > 0:
                content = resp.content.split('|')
                if len(content) == 2 and content[0] == mobile:
                    mobile, code = content[0], content[1]
                else:
                    LOG.error("Yma get verify code resp.content format error, "
                              "content=%s", content)

        return code
        
    def add_to_black(self, mobile=None):
        if not mobile:
            return

        if not self.logined:
            self.login()

        if not self.logined:
            raise Exception("Yma not login")

        payload = {
            "action": "addIgnoreList",
            "token": self.token,
            "pid": self.pid,
            "uid": self.user,
            "mobiles": mobile,
        }
        resp = self._get(settings.YMA_HOST, payload=payload)       
        LOG.debug("yma add %s to black return: %s", mobile, resp.content)
        if not resp.ok:
            LOG.warning("Yma add %s to black failed, return: %s",
                         mobile, resp.content)
            

if __name__ == "__main__":
    yma = YmaApi(settings.YMA_USER,
                settings.YMA_USER_PWD,
                settings.YMA_PID)
    #yma.get_mobiles(YMA_BATCH_MOBILE)

    while True:
        import time
        time.sleep(5)
        yma.get_verify_code("17186426278")


API =  YmaApi(settings.YMA_USER, settings.YMA_USER_PWD, settings.YMA_PID)
