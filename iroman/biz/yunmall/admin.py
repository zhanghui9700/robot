#-*- coding=utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import (Fish, ExcceedCode, ExcceedMobile, Config)


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


admin.site.register(Fish, FishAdmin)
admin.site.register(ExcceedMobile, ExcceedMobileAdmin)
admin.site.register(Config, ConfigAdmin)
