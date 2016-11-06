#-*- coding=utf-8 -*-

from rest_framework import generics, status

from common.pagination import PagePagination

from biz.yunmall.models import ExcceedMobile
from biz.yunmall.serializer import ExcceedMobileSerializer


class BlackList(generics.ListAPIView):
    queryset = ExcceedMobile.living.all()
    serializer_class = ExcceedMobileSerializer
    pagination_class = PagePagination

    def get_queryset(self):
        queryset = super(BlackList, self).get_queryset() 
        return queryset.order_by("-id")