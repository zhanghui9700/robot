#-*- coding=utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import (Fish, ExcceedCode, ExcceedMobile, Config,
                    IPPool, IPBlack)


class FishAdmin(admin.ModelAdmin):    
    list_display = ("username", "mobile", "code", "parent", "child_count", 
                    "password", "pay_password", "nickname", "id_card", "email",
                    "create_date", "step")

    class Meta:
        model = Fish


class ExcceedMobileAdmin(admin.ModelAdmin):
    list_display = ("mobile", "create_date")

    class Meta:
        model = ExcceedMobile


class ConfigAdmin(admin.ModelAdmin):
    list_display = ("conf", "value", "description")

    class Meta:
        model = Config


class IPPoolAdmin(admin.ModelAdmin):
    list_display = ("ip_str", "count", "create_date")

    class Meta:
        model = IPPool


class IPBlackAdmin(admin.ModelAdmin):
    list_display = ("get_ip", "get_mobile", "create_date")

    def get_ip(self, obj):
        return obj.ip.ip_str

    def get_mobile(self, obj):
        return obj.fish.mobile

    get_ip.short_description = _('IP')
    get_mobile.short_description = _("Mobile")

    class Meta:
        model = IPBlack


admin.site.register(Fish, FishAdmin)
admin.site.register(ExcceedMobile, ExcceedMobileAdmin)
admin.site.register(Config, ConfigAdmin)
admin.site.register(IPPool, IPPoolAdmin)
admin.site.register(IPBlack, IPBlackAdmin)
