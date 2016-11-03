#-*- coding=utf-8 -*-

import csv
import datetime
import logging
import requests
import time
import os
from optparse import make_option

from django.conf import settings
from django.core.management import BaseCommand

from biz.yunmall.models import Fish

LOG = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "python manage.py export_csv"

    def _write_csv(self):
        now = datetime.datetime.now()
        name = "%s-user.csv" % now.strftime("%Y-%m-%d-%H-%M")
        csv_file = os.path.join(settings.BASE_DIR, '..', 'tools', name)
        meta = {
            'file': csv_file,
            'class': Fish,
            'fields': ("username", "mobile", "password", "pay_password", 
                        "parent", "code", "nickname", "id_card", 
                        "email", "create_date", "child_count")
        }
 
        with open(meta['file'], 'w+') as f:
            writer = csv.writer(f)
            #writer.write(new Buffer('\xEF\xBB\xBF','binary'))
            writer.writerow(meta['fields'])
            for obj in meta['class'].living.all():
                row = [
                    unicode(getattr(obj, "username")),
                    unicode(getattr(obj, "mobile")),
                    unicode(getattr(obj, "password")),
                    unicode(getattr(obj, "pay_password")),
                    unicode(getattr(obj, "parent")),
                    unicode(getattr(obj, "code")),
                    obj.nickname.encode("utf-8") if obj.nickname else None,
                    unicode(getattr(obj, "id_card")),
                    unicode(getattr(obj, "email")),
                    unicode(getattr(obj, "create_date")\
                                    .strftime("%Y-%m-%d:%H-%M-%S")),
                    unicode(getattr(obj, "child_count")),
                ]
                writer.writerow(row)
        print 'save csv file to %s' % meta['file']

    def handle(self, *args, **kwargs):
        try:
            self._write_csv()
        except Exception as ex:
            raise ex
        else:
            print "Export succeed."
