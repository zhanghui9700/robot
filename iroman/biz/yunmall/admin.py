#-*- coding=utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


from .models import Fish

class FishAdmin(admin.ModelAdmin):    
    list_display = ("username", "mobile", "code", "child_count", "password",
                    "pay_password", "nickname", "id_card", "email",
                    "create_date", "step")

    class Meta:
        model = Fish

admin.site.register(Fish, FishAdmin)
