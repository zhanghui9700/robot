#-*- coding=utf-8 -*-

import datetime
import logging
import requests
import time
from optparse import make_option

from django.conf import settings
from django.core.management import BaseCommand

from ._target import OrderTarget

LOG = logging.getLogger(__name__)



class Command(BaseCommand):
    help = "python manage.py excel"

    def _prepare_target(self):
        """
        return {"category": [product_id, product_id]}
        """
        t = OrderTarget(path=settings.EXCEL_PATH)
        return t
         
    def handle(self, *args, **kwargs):
        target = self._prepare_target()
        print "excel: ", target.target
        print target.construct()
