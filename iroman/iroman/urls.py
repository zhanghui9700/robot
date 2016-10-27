#-*- coding=utf-8 -*-

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = []

urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
]
