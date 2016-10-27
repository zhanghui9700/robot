#-*- coding=utf-8 -*-

import datetime
import logging
import requests
import time
from optparse import make_option

from django.conf import settings
from django.core.management import BaseCommand

from biz.yunmall.utils import Yunmall

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
        yunmall = Yunmall(invate_code)
        yunmall.start()
   
    def handle(self, *args, **kwargs):
        begin = datetime.datetime.now()
        LOG.info("*"*30)
        try:
            self.run(kwargs.get("code", None))
        except Exception as ex:
            LOG.exception("yunmall.run raise exception.")

        end = datetime.datetime.now()
        LOG.info("yunmall.run end, xapply %s seconds",
                  (end-begin).seconds)
        LOG.info("#"*30)
