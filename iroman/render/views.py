#-*- coding=utf-8 -*-

import logging
import urlparse
import json

from django.conf import settings
from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import (HttpResponseRedirect,
                         JsonResponse,
                         HttpResponseForbidden)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from common.decorators import superuser_required

LOG = logging.getLogger(__name__)


@login_required
def index(request):
    if request.user.is_superuser:
        return redirect('management')
    else:
        return redirect("dashboard")


@login_required
def dashboard(request):
    if request.user.is_superuser:
        return redirect('management')

    return render(request, "dashboard.html")


@superuser_required
def management(request):
    return render(request, 'management.html')


class LoginView(View):

    def get(self, request):
        return self.response(request)

    def post(self, request):
        form = AuthenticationForm(data=request.POST)

        if not form.is_valid():
            return self.response(request, form)

        user = form.get_user()
        auth_login(request, user)

        return HttpResponseRedirect(reverse("dashboard"))

    def response(self, request, form=None):

        if form is None:
            form = AuthenticationForm(initial={'username': ''})
            error = False
        else:
            error = True

        return render(request, 'login.html', {
            "form": form,
            "error": error
        })


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("index"))



@login_required
def site_config(request):
    user = request.user
    current_user = {
        'id': user.id,
        'username': user.username,
        'is_superuser': user.is_superuser,
    }

    return render(request, 'site_config.js',
                  {'current_user': json.dumps(current_user),
                   'site_config': json.dumps(settings.SITE_CONFIG)},
                  content_type='application/javascript')


def not_found(request):
    if request.path.startswith('/api'):
        return JsonResponse({"success": False,
                             "msg": ugettext("Data not found!")},
                            status=404)

    return render(request, '404.html')


def server_error(request):
    if request.path.startswith('/api'):
        return JsonResponse({"success": False,
                             "msg": ugettext("System Error!")},
                            status=500)

    return render(request, '500.html')