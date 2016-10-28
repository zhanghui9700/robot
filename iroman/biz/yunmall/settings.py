#-*- coding=utf-8-*-

from django.utils.translation import ugettext as _

from common.complex_choice import ComplexChoice


class CONFIG(ComplexChoice):
    PAUSED_CHOICE = ComplexChoice.choice("paused", _("Paused"))
    DAY_QUOTA_CHOICE = ComplexChoice.choice("day_quota", _("Day Quota"))


class VERIFY_CODE(ComplexChoice):
    OK_CHOICE = ComplexChoice.choice(90001, _("OK"))
    FAILED_CHOICE = ComplexChoice.choice(90002, _("Failed"))


class SMS_SEND_CODE(ComplexChoice):
    OK_CHOICE = ComplexChoice.choice(5, _("OK"))
    FREQUENCY_CHOICE = ComplexChoice.choice(7, _("SMS Frequenct"))
    REGISTED_CHOICE = ComplexChoice.choice(23, _("Mobile Registed"))
    USER_NOT_EXIST_CHOICE = ComplexChoice.choice(36, _("User Not Exist"))
    IMAGE_ERROR_CHOICE = ComplexChoice.choice(20001, _("Image Code Error"))
    USER_CONFLICT_CHOICE = ComplexChoice.choice(50002, _("USER CONFLICT"))


class REGISTER_CODE(ComplexChoice):
    SUCCEED_CHOICE = ComplexChoice.choice(26, _("Succeed"))
    FAILED_CHOICE = ComplexChoice.choice(27, _("Failed"))
    USERNAME_CONFLICT_CHOICE = ComplexChoice.choice(21, _("UserName Conflict"))
    MOBILE_CONFLICT_CHOICE = ComplexChoice.choice(23, _("Mobile Conflict"))
    MAIL_FORMAT_ERROR_CHOICE = ComplexChoice.choice(25, _("Mail Format Error"))
    MOBILE_FORMAT_ERROR_CHOICE = ComplexChoice.choice(4, _("Mobile Format Error"))
    SMS_CODE_ERROR_CHOICE = ComplexChoice.choice(2, _("SMS Code Incorrect"))
    SMS_CODE_EXPIRED_CHOICE = ComplexChoice.choice(1, _("SMS Code Expired"))
    MAIL_EXIST_CHOICE = ComplexChoice.choice(28, _("Mail Exist"))
    PASSWORD_FORMAT_ERROR_CHOICE = ComplexChoice.choice(29, _("Password Format Error"))
    PASSWORD_TOO_SAMPLE_CHOICE = ComplexChoice.choice(204, _("Password Too Sample"))
    INVATE_ERROR_CHOICE = ComplexChoice.choice(202, _("Invate Error"))
    IMAGE_ERROR_CHOICE = ComplexChoice.choice(20001, _("Image Code Error"))


class LOGIN_RESULT(ComplexChoice):
    OK_CHOICE = ComplexChoice.choice(31, _("OK"))
    FAILED_CHOICE = ComplexChoice.choice(32, _("Failed"))
    PASSWORD_ERROR_CHOICE = ComplexChoice.choice(33, _("Password Error"))
    LOCKED_CHOICE = ComplexChoice.choice(35, _("Locked"))
    DEVICE_ONLY_CHOICE = ComplexChoice.choice(311, _("Device Only"))


class BASIC_INFO_RESULT(ComplexChoice):
    OK_CHOICE = ComplexChoice.choice(90001, _("OK"))
    USERNAME_CONFLICT_CHOICE = ComplexChoice.choice(21, _("UserName Conflict"))
    NICKNAME_CONFLICT_CHOICE = ComplexChoice.choice(22, _("NickName Conflict"))
    MAIL_EXIST_CHOICE = ComplexChoice.choice(28, _("Mail Exist"))
    MAIL_FORMAT_ERROR_CHOICE = ComplexChoice.choice(25, _("Mail Format Error"))
 

class PAY_INFO_RESULT(ComplexChoice):
    OK_CHOICE = ComplexChoice.choice(90001, _("OK"))
    FAIELD_CHOICE = ComplexChoice.choice(90002, _("Set Paypassword Faield"))
    IMAGE_ERROR_CHOICE = ComplexChoice.choice(20001, _("Image Code Error"))
