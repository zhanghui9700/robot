#-*- coding=utf-8 -*-

import logging
from smtplib import SMTPException

from django.conf import settings
from django.core.management import BaseCommand
from django.core.mail import send_mail

LOG = logging.getLogger(__name__)

class Command(BaseCommand):

    def _log(self, tag, result):
        label = self.style.ERROR("XXX")
        if result:
            label = self.style.MIGRATE_SUCCESS(":-)")

        self.stdout.write("{:<30}{:<5}".format(tag, label))

    def _check_mail(self):
        if len(settings.ADMINS) < 1:
            self._log("CHECK_MAIL No Admin", False)
            return

        try:
            title = "%sCheck Settings" % settings.EMAIL_SUBJECT_PREFIX
            msg = "This message used for checking email settings."
            result = send_mail(title, msg,
                        settings.DEFAULT_FROM_EMAIL, [settings.ADMINS[0]])
        except SMTPException as e:
            result = False

        self._log("CHECK_MAIL", result)

    def handle(self, *args, **kwargs):
        self.stdout.write(__name__)
        self.stdout.write(self.style.WARNING("************CHECK START************"))
        self._check_mail()
        self.stdout.write(self.style.WARNING("************CHECK  END*************"))
