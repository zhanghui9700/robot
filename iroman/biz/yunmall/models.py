#-*- coding=utf-8 -*-

from datetime import date

from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.models import BaseModel

from .settings import CONFIG

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
        if cls.living.filter(child_count__lt=26).exclude(code=None).exists():
            return cls.living.filter(child_count__lt=26).exclude(code=None).first()
        return None

    @classmethod
    def get_fresher(cls):
        if cls.living.filter(code=None).exists():
            return cls.living.filter(code=None).first()
        return None

    @classmethod
    def mark_excceed(cls, code=None):
        if not code:
            return
        cls.living.filter(code=code).update(child_count=26)
        ExcceedCode.living.create(code=code)

    @classmethod
    def today_reg_count(cls):
        today = date.today()
        return cls.living.filter(create_date__gte=today).count() 
    
    @classmethod
    def new(cls, invate_code, username, pwd, mobile):
        parent = cls.living.get_or_none(code=invate_code)

        obj = cls.living.create(parent=parent,
                                mobile=mobile,
                                username=username,
                                password=pwd,)

        if parent:
            parent.child_count = parent.child_count + 1
            parent.save()
        return obj

    def __unicode__(self):
        return u"Code:%s Mobile:%s" % (self.code, self.mobile)

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


class ExcceedMobile(BaseModel):
    mobile = models.CharField(max_length=32, unique=True) 

    @classmethod
    def exist(cls, mobile):
        return cls.living.filter(mobile=mobile).exists()

    @classmethod
    def record(cls, mobile):
        if cls.living.filter(mobile=mobile).exists():
            return
        try:
            cls.living.create(mobile=mobile)
        except:
            pass

    class Meta:
        db_table = "yunmall_excceed_mobile"
        verbose_name = _("Excceed Mobile")
        verbose_name_plural = _("Excced Mobile")


class Config(BaseModel):
    conf = models.CharField(_("Config"), max_length=128,
                    unique=True, choices=CONFIG.CHOICES)
    value = models.CharField(_("Value"), max_length=128)
    description = models.CharField(_("Description"), max_length=128)

    @classmethod
    def get_conf(cls, conf):
        if cls.living.filter(conf=conf).exists():
            return cls.living.filter(conf=conf).first()

        return None

    def __unicode__(self):
        return u"<%s  %s=%s>" % (self.description, self.conf, self.value)

    class Meta:
        db_table = "yunmall_config"
        verbose_name = _("Config")
        verbose_name_plural = _("Config") 
