# -*- coding=utf-8 -*-

import logging
import hashlib
import urllib
import json
import base64
import requests

from django.conf import settings

LOG = logging.getLogger(__name__)


def md5str(string): 
    """
    md5加密字符串
    """
    m = hashlib.md5(string)
    return m.hexdigest()


def md5byte(byte):
    """
    md5加密byte
    """
    return hashlib.md5(byte).hexdigest()


class DamatuApi():
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.balance = 0

    def getSign(self, param=b''):
        byte = bytes(settings.DM2_DEV_KEY) + bytes(self.username) + param
        return (md5byte(byte))[:8]

    def getPwd(self):
        username_md5 = md5str(self.username)
        pwd_md5 = md5str(self.password)
        username_pwd_md5_contract = md5str(username_md5+pwd_md5)
        pwd = md5str(settings.DM2_DEV_KEY + username_pwd_md5_contract)
        return pwd
         
    def post(self, path, params=None):
        url = settings.DM2_HOST + path
        resp = requests.post(url, data=params)
        LOG.info("[dama2] post url %s return: %s", url, resp.status_code)
        if resp.status_code in [200, 201, 202]:
            return resp.json()
        else:
            LOG.info("[dama2] post url: %s, params: %s", url, params)

    def get_balance(self):
        """
        查询余额 return 是正数为余额 如果为负数 则为错误码
        """
        data = {
            'appID': settings.DM2_APP_ID,
            'user': self.username,
            'pwd': self.getPwd(),
            'sign': self.getSign()
        }
        res = self.post('d2Balance', data)
        if res['ret'] == 0:
            self.balance = res["balance"]
            LOG.info("[dama2] get balance succeed, balance: %s" % res['balance'])
            return res["balance"]
        else:
            self.balance = 0
            LOG.info("[dama2] get balance error, ret: %s" % res['ret'])
            return res['ret']

    def decode(self, filePath, type):
        """ 
        上传验证码 
        filePath 验证码图片路径 如d:/1.jpg 
        type是类型，查看http://wiki.dama2.com/index.php?n=ApiDoc.Pricedesc
        return 是答案为成功 如果为负数 则为错误码
        """
        if self.balance <=0:
            self.get_balance()

        if self.balance <= 0:
            raise Exception("Dama2 balance is 0.0 !!!")

        with open(filePath, 'rb') as f:
            fdata = f.read()
            filedata = base64.b64encode(fdata)

        data = {
            'appID': settings.DM2_APP_ID,
            'user': self.username,
            'pwd': self.getPwd(),
            'type': type,
            'fileDataBase64': filedata,
            'sign': self.getSign(fdata)
        }

        # jres format: {
        #    u'sign': u'ad454717', 
        #    u'id': 1401372945, 
        #    u'ret': 0, 
        #    u'result': u'2'
        #}
        jres = self.post('d2File', data)
        LOG.info("[dama2] decode image response: %s", jres)
        if jres['ret'] == 0:
            return True, jres['result']
        else:
            return False, jres['id']

    def reportError(self, id):
        """
        报错
        参数id(string类型)由上传打码函数的结果获得
        return 0为成功 其他见错误码
        """
        data = {
            'appID':settings.DM2_APP_ID,
            'user': self.username,
            'pwd': self.getPwd(),
            'id': id,
            'sign': self.getSign(id)
        }
        jres = self.post('d2ReportError', data)
        LOG.info("[dama2] report error response: %s", jres)
        return jres['ret']


if __name__ == "__main__":
    dmt = DamatuApi(settings.DM2_NORMAL_USER,
                    settings.DM2_NORMAL_USER_PWD)
    balance = dmt.get_balance()
    if balance > 0:
        succeed, result = dmt.decode('0.87036439137.png', 106)  # 上传打码
        if succeed:
            print "decode succeed, result: " + result
        else:
            dmt.reportError(result)
            print "decode failed, report error.."


API = DamatuApi(settings.DM2_NORMAL_USER, settings.DM2_NORMAL_USER_PWD)
