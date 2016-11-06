#-*- coding=utf-8 -*-

from django.utils.translation import ugettext_lazy as _

def get_i18n():
    return {
        "summary": unicode(_("Overview Summay")),
        "registered_total": unicode(_("Registered Total")),
        "registered_today": unicode(_("Registered Today")),
        "mobile_black_total": unicode(_("Mobile Black Total")),
        "mobile_black_today": unicode(_("Mobile Black Today")),
        "recent_registered": unicode(_("Recent Registered User")),
        "recent_mobile_black": unicode(_("Recent Mobile Black")),
    }