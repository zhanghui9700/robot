#-*- coding=utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from render import views

urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        url(r'^admin/', include(admin.site.urls)),
    ]

urlpatterns += [
    url(r'^api/', include('biz.urls')),
]

urlpatterns += patterns(
    '',
    url(r'^$', views.index, name="index"),
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    url(r'^management/$', views.management, name="management"),
    url(r'^site-config.js$', views.site_config, name="site_config"),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.logout, name='logout'),
)

handler404 = views.not_found
handler500 = views.server_error
