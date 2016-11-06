#-*- coding=utf-8 -*-

from rest_framework import generics, status

from common.pagination import PagePagination

from biz.yunmall.models import Fish
from biz.yunmall.serializer import FishSerializer


class FishList(generics.ListAPIView):
    queryset = Fish.living.all()
    serializer_class = FishSerializer
    pagination_class = PagePagination

    def get_queryset(self):
        queryset = super(FishList, self).get_queryset() 
        return queryset.order_by("-id")