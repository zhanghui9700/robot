#-*- coding=utf-8 -*-

import datetime
import logging
import requests
import time
from optparse import make_option

from django.conf import settings
from django.core.management import BaseCommand

from ._browser import SeleniumBrowser

LOG = logging.getLogger(__name__)



class Command(BaseCommand):
    help = "python manage.py login"
         
    def handle(self, *args, **kwargs):
        with SeleniumBrowser() as browser:
            browser.login()
            kill = raw_input("input [Enter] to exits") 

 
