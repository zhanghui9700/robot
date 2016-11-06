#-*- coding=utf-8 -*-

from django.conf.urls import patterns, include, url

from biz.i18n import views as i18n_views

urlpatterns = [
	url(r'^i18n/(?P<lang>(cn)|(en){1}).json$', i18n_views.I18N.as_view()),
]

urlpatterns += [
    url(r'^yunmall/', include("biz.yunmall.urls")),
]