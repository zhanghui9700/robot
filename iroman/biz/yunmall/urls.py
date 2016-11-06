#-*- coding=utf-8 -*-

from django.conf.urls import url, include

from biz.yunmall.views import overview
from biz.yunmall.views import fish
from biz.yunmall.views import mobile_black

overview_urls = [
	url(r'^summary/$', overview.Summary.as_view(), name="overview-summary"),
]

fish_urls = [
	url(r'^$', fish.FishList.as_view(), name="fish-list"),
]

mobile_black_urls = [
	url(r'^$', mobile_black.BlackList.as_view(), name="mobile-black-list"),
]

urlpatterns = [
    url(r'^overview/', include(overview_urls)),
    url(r'^fish/', include(fish_urls)),
    url(r'^mobile-black/', include(mobile_black_urls)),
]