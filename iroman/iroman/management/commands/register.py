#-*- coding=utf-8 -*-

import datetime
import logging
import requests
import time
from optparse import make_option

from django.conf import settings
from django.core.management import BaseCommand

from common.utils import get_host_ip
from biz.yunmall.models import IPPool, IPBlack
from biz.yunmall.tools.register import YunmallRegister

LOG = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "python manage.py yunmall --code <Invate Code>"

    option_list = BaseCommand.option_list + (
        make_option('--code',
            action='store',
            dest='code',
            type=int,
            nargs=1,
            help='Invate code to register.'),
        )

    def run(self, ip_str, invate_code=None):
        yunmall = YunmallRegister(ip_str, invate_code)
        return  yunmall.start()
   
    def handle(self, *args, **kwargs):
        begin = datetime.datetime.now()
        LOG.info("%s%s%s", "*"*15, "regiseter.start", "*"*15)
        succeed = False
        try:
            ip_str = None
            if getattr(settings, "SWITCH", False):
                while True:
                    time.sleep(1)
                    ip_str = get_host_ip()
                    if ip_str:
                        break
                IPPool.record(ip_str)
                if IPBlack.exist(ip_str):
                    raise Exception("IP %s in black list.")
            succeed = self.run(ip_str, kwargs.get("code", None))
        except Exception as ex:
            LOG.exception("register.run raise exception.")

        end = datetime.datetime.now()
        LOG.info("register.run end, xapply %s seconds, result: %s",
                  (end-begin).seconds, succeed)
        LOG.info("%s%s%s", "#"*15, "regiseter.end", "#"*15)
