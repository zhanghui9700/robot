#-*- coding=utf-8 -*-

from django.utils.translation import ugettext_lazy as _

def get_i18n():
    return {
        "console": unicode(_("Console")),
        "overview": unicode(_("Overview")),
        "users": unicode(_("Users")),
        "black_mobile": unicode(_("Mobile Black")),
    }