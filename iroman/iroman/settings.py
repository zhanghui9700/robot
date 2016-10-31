""" Django settings for iroman project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import logging
import logging.config
import os
import random
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except:
    pass




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yi_q+a4iew$)6=xl!v*b(p10^0#c)2)xl0a27pfjnfanbjt-t0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ["*",]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'iroman',
    'biz',
    'biz.yunmall',
    'render',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'iroman.urls'

WSGI_APPLICATION = 'iroman.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '..', 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh_CN'
TIME_ZONE = 'Asia/Shanghai'
DATETIME_FORMAT="Y-m-d H:i:s"
DEFAULT_CHARSET="utf-8"
USE_I18N = True
USE_L10N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
LOGIN_URL = '/login'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
            ],
        },
    },
]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)


LOG_PATH = os.path.join(BASE_DIR, '..', 'logs', 'robot.log')
LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        "verbose": {
            'format': '%(asctime)s %(levelname)s %(process)d -- %(message)s',
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'filters': None,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename':  LOG_PATH,
            'formatter': 'verbose'
        },

        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },

        'mail_admin': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': False,
        },
    },
    'loggers': {
        'iroman': {
            'handlers': ['default', 'mail_admin'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'biz': {
            'handlers': ['default', 'mail_admin'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['default', ],
            'level': 'ERROR',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['default'],
        'level': 'INFO' if DEBUG else 'ERROR',
    },
}

try:
    from local.local_settings import *
except (ImportError, ImportWarning) as e:
    print "\033[44;37m ###################################### \033[0m"
    print "\033[44;37m                                        \033[0m"
    print "\033[44;37m                                        \033[0m"
    print "\033[44;37m        No local settings exist         \033[0m"
    print "\033[44;37m      path: local/local_settings.py     \033[0m"
    print "\033[44;37m     if you want to custom settings     \033[0m"
    print "\033[44;37m create local_settings.py and config it.\033[0m"
    print "\033[44;37m                                        \033[0m"
    print "\033[44;37m                                        \033[0m"
    print "\033[44;37m ###################################### \033[0m"


logging.config.dictConfig(LOG_CONFIG)

__YMA = YMA_LIST[random.randint(0, len(YMA_LIST) - 1)]

YMA_USER = __YMA.get("YMA_USER", "adyvicki")
YMA_USER_PWD = __YMA.get("YMA_USER_PWD", "12ab!@")
YMA_PID = __YMA.get("YMA_PID", "14022")
