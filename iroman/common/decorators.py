#-*- coding=utf-8 -*-

import logging
from functools import wraps

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

LOG = logging.getLogger(__name__)


def superuser_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME,
                       login_url=None):
    """
    Decorator for views that checks that the user is logged in and is super user,
    redirecting to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

require_GET = api_view(["GET"])
require_POST = api_view(["POST"])
require_DELETE = api_view(["DELETE"])
require_PUT = api_view(["PUT"])


def api_enabled(enabled):

    def decorator(func):
        @wraps(func)
        def wrapped_view(*args, **kwargs):
            if enabled:
                return func(*args, **kwargs)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

        return wrapped_view

    return decorator


def jsonify(func):

    @wraps(func)
    def wrapped_view(*args, **kwargs):
        return Response(func(*args, **kwargs))

    return wrapped_view


def debug(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        try:
            result = func(*args, **kwargs)
            print result
            return result
        except Exception as e:
            print e
            raise  e

    return wrapper


def timing(func):

    @wraps(func)
    def wrap(*args, **kwargs):
        begin = timezone.now()
        LOG.info("[%s] invoke start.", func.func_name)
        ret = func(*args, **kwargs)
        end = timezone.now()
        cost = end - begin
        LOG.info("[%s] invoke end, apply [%s] seconds",
                    func.func_name, cost.seconds)
        return ret

    return wrap
