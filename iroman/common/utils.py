#-*- coding=utf-8 -*-

import os
import csv
import random
import string
import socket
import time

from django.conf import settings

from common import randname

try:
    from .api.damatu import API as dama_api
    from .api.yma import API as yma_api
    from .api.tm import API as tm_api
except Exception as ex:
    raise ex
else:
    DAMA_API = dama_api  
    if getattr(settings, "YMA_ENABLED", True):
        MOBILE_API = yma_api

    if getattr(settings, "TM_ENABLED", False):
        MOBILE_API = tm_api
 

def ip2int(ip_str):
    ip_int = 0
    i = 3
    numbers = str(ip_str).split('.')
    for num in numbers:
        ip_int += int(num) * (256 ** i) # or pow(256, i)
        i -= 1
    return ip_int   
 

def int2ip(ip_int):
    ip_str = ''
    left_value = ip_int
    for i in [3, 2, 1, 0]:
        ipTokenInt = left_value / 256**i
        ip_str = ip_str + str(ipTokenInt)
        if i!=0:
            ip_str = ip_str + '.'
        left_value %= 256**i
    return ip_str  


def get_host_ip():
    ip = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("baidu.com", 80))
        ip = s.getsockname()[0]
        s.close()  
    except:
        pass
    return ip


def gen_username(length=8):
    seed = string.ascii_lowercase + string.digits
    return ''.join(random.choice(seed) for _ in range(length))


def gen_basic_info(): 
    email, id_card, nick_name, pwd = None, None, None, "pAssw0rd"
    email = randname.email() 
    id_card = randname.id_card()
    nick_name = randname.nickname()
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
