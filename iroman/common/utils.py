#-*- coding=utf-8 -*-

import os
import csv
import random
import string
import time

from .api.damatu import API as dama_api
from .api.yma import API as yma_api

from common import randname


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


DAMA_API = dama_api
MOBILE_API = yma_api
