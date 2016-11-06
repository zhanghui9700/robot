#-*- coding=utf-8 -*-

import json

from django.conf import settings
from rest_framework import serializers

from biz.yunmall.models import Fish, ExcceedMobile


class FishSerializer(serializers.ModelSerializer):
    parent_mobile = serializers.SerializerMethodField()
    def get_parent_mobile(self, obj):
        if obj.parent:
		    return obj.parent.mobile
        else:
            return u"N/A"

    class Meta:
        model = Fish



class ExcceedMobileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExcceedMobile