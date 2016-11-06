#-*-coding-utf-8-*-

import logging

from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticated, IsAdminUser)
from rest_framework.decorators import permission_classes

from common import utils
from biz.yunmall.models import Fish, ExcceedMobile


class Summary(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, *args, **kwargs):
        data = {
            "fish_total": Fish.living.count(),
            "fish_today": Fish.today_reg_count(),
            "mobile_black_total": ExcceedMobile.living.count(),
            "mobile_black_today": ExcceedMobile.today_count(),
        }
        return utils.json(data)