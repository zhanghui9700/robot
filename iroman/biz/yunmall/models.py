#-*- coding=utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.models import BaseModel

STEP_CHOICES = (
    (0, _("Error")),
    (1, _("Register")),
    (2, _("Profile")),
    (3, _("Pay Password")),  
    (99, _("Succeed")),
)

class Fish(BaseModel): 
    code = models.CharField(_("Invate Code"), max_length=128,
                            unique=True, null=True) 
    username = models.CharField(_("Name"), max_length=128)
    mobile = models.CharField(_("Mobile"), max_length=32)
    password = models.CharField(_("Password"), max_length=32)
    pay_password = models.CharField(_("Pay Password"), max_length=32, null=True)

    parent = models.ForeignKey("self", db_constraint=False,
                                null=True, blank=True) 
    child_count = models.IntegerField(_("Child"), default=0)

    nickname = models.CharField(_("Chinese Name"), max_length=128, null=True)
    id_card = models.CharField(_("Chinese ID"), max_length=128, null=True)
    email = models.EmailField(_("Email"), null=True, max_length=128)

    step = models.IntegerField(_("Process"), default=1, choices=STEP_CHOICES)

    class Meta:
        db_table = "yunmall_fish"
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")

    @classmethod
    def get_invator(cls):
        if cls.living.filter(child_count__lt=26).exists():
            return cls.living.filter(child_count__lt=26).first()

    @classmethod
    def mark_excceed(cls, code=None):
        if not code:
            return
        cls.living.filter(code=code).update(child_count=26)
        ExcceedCode.living.create(code=self.code)

    def fake_delete(self):
        self.deleted = True
        self.update()


class ExcceedCode(BaseModel):
    code = models.CharField(max_length=128, unique=True) 

    @classmethod
    def exist(cls, code):
        return cls.living.filter(code=code).exists()


    class Meta:
        db_table = "yunmall_excceed_code"
        verbose_name = _("Excceed Code")
        verbose_name_plural = _("Excced Codes")
