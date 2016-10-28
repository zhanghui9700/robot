#-*- coding=utf-8 -*-

import datetime
import logging
import requests
import time
from optparse import make_option

from django.conf import settings
from django.core.management import BaseCommand

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

    def run(self, invate_code=None):
        yunmall = YunmallRegister(invate_code)
        return  yunmall.start()
   
    def handle(self, *args, **kwargs):
        begin = datetime.datetime.now()
        LOG.info("%s%s%s", "*"*15, "regiseter.start", "*"*15)
        succeed = False
        try:
            succeed = self.run(kwargs.get("code", None))
        except Exception as ex:
            LOG.exception("register.run raise exception.")

        end = datetime.datetime.now()
        LOG.info("register.run end, xapply %s seconds, result: %s",
                  (end-begin).seconds, succeed)
        LOG.info("%s%s%s", "#"*15, "regiseter.end", "#"*15)
