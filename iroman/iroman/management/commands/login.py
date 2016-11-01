#-*- coding=utf-8 -*-

import datetime
import logging
import requests
import time
from optparse import make_option

from django.conf import settings
from django.core.management import BaseCommand

from biz.yunmall.models import Fish
from biz.yunmall.tools.login import YunmallLogin, SeleniumLogin

LOG = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "python manage.py login"

    def run(self):
        result = False
        fresher = Fish.get_one_blocked() 
        if fresher:
            LOG.info("get auto login fresher: %s", fresher)
            phpsessid = None
            with SeleniumLogin(fresher) as robot:
                robot.get_login_session()
                phpsessid = robot.PHPSESSID
           
            if phpsessid:
                login = YunmallLogin(fresher, 'PHPSESSID=%s' % phpsessid)
                result = login.start()
        else:
            LOG.info("no more fresher should submit info, exist")
        
        return result
   
    def handle(self, *args, **kwargs):
        begin = datetime.datetime.now()
        LOG.info("%s%s%s", "*"*15, "login.start", "*"*15)
        succeed = False
        try:
            succeed = self.run()
        except Exception as ex:
            LOG.exception("login.run raise exception.")

        end = datetime.datetime.now()
        LOG.info("login.run end, xapply %s seconds, result: %s",
                  (end-begin).seconds, succeed)
        LOG.info("%s%s%s", "#"*15, "login.end", "#"*15)
