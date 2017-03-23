#-*- coding=utf-8 -*-

import datetime
import logging
import requests
import time
from optparse import make_option

from django.conf import settings
from django.core.management import BaseCommand

from .browser import SeleniumBrowser
from .target import OrderTarget

LOG = logging.getLogger(__name__)



class Command(BaseCommand):
    help = "python manage.py order"

    def _prepare_target(self):
        """
        return {"category": [product_id, product_id]}
        """
        t = OrderTarget(path=settings.EXCEL_PATH)
        return t

    def run(self, target=None):
        if not target:
            return False

        with SeleniumBrowser() as browser:
            browser.auto_order(target)
        
        return True

    def _check_time(self):
        now = datetime.datetime.utcnow()
        if now.hour >= 13 or now.hour < 3:
            return True
        else:
            return False
        
   
    def handle(self, *args, **kwargs):
        LOG.info("%s%s%s", "#"*15, "ptx.start", "#"*15)
        begin = datetime.datetime.now()
        succeed = False
        if self._check_time():
            try:
                target = self._prepare_target()
                succeed = self.run(target.construct())
                target.mark_complete()
            except Exception as ex:
                LOG.exception("ptx.run raise exception.")
        else:
            LOG.info("ptx.run time not allowed.")

        end = datetime.datetime.now()
        LOG.info("ptx.run end, xapply %s seconds, result: %s",
                  (end-begin).seconds, succeed)
        LOG.info("%s%s%s\n", "#"*15, "ptx.end", "#"*17)
