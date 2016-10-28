#-*- coding=utf-8 -*-

import os
import csv
import random
import string
import time

from .api.damatu import API as dama_api
from .api.yma import API as yma_api

COMMON_DIR = os.path.dirname(__file__)

def gen_username(length=8):
    seed = string.ascii_lowercase + string.digits
    return ''.join(random.choice(seed) for _ in range(length))


def _gen_id_card():
    ARR = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
    LAST = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')

    t = time.localtime()[0]
    x = '%02d%02d%02d%04d%02d%02d%03d' %(random.randint(10,99),
                                        random.randint(01,99),
                                        random.randint(01,99),
                                        random.randint(t - 80, t - 18),
                                        random.randint(1,12),
                                        random.randint(1,28),
                                        random.randint(1,999))
    y = 0
    for i in range(17):
        y += int(x[i]) * ARR[i]

    return '%s%s' %(x, LAST[y % 11])


def gen_basic_info():
    def _random_name():
        first = u"李王张刘陈杨黄赵吴周孙马朱胡郭何高林罗郑梁谢宋唐许韩冯邓曹彭曾肖田董袁潘于蒋蔡余杜叶程苏魏吕丁任沈姚卢姜崔锺谭陆汪范金石赖廖贾夏韦傅方白邹孟熊秦邱江尹薛闫段雷侯龙史陶黎贺顾毛郝龚邵万钱严覃武戴莫孔向汤"
        nick_name = first[random.randrange(len(first)-1)] + unichr(random.randint(0x4E00, 0x9FBF)) + unichr(random.randint(0x4E00, 0x9FBF))
        return nick_name
        
    email, id_card, nick_name, pwd = None, None, None, "pAssw0rd"
    seed = ''.join(random.choice(string.digits) for _ in range(9))
    email = "%s@qq.com" % seed
    id_card = _gen_id_card()
    nick_name = _random_name()

    return email, id_card, nick_name, pwd


TRUE_STRINGS = ('1', 't', 'true', 'on', 'y', 'yes')
FALSE_STRINGS = ('0', 'f', 'false', 'off', 'n', 'no')


def bool_from_string(string=None):
    if not string:
        return False

    if isinstance(string, bool):
        return string

    lowered = string.strip().lower()

    if lowered in TRUE_STRINGS:
        return True
    elif lowered in FALSE_STRINGS:
        return False 
    else:
        return False


DAMA_API = dama_api
MOBILE_API = yma_api
