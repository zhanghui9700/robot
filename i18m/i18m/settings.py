"""
Django settings for i18m project.

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
SECRET_KEY = '!s7@qar)fc9flk5l+w5$0!vxwc-udy#4gs1$+k1y-tti9x&659'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'i18m',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'i18m.urls'

WSGI_APPLICATION = 'i18m.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


##################################

LOG_PATH = os.path.join(BASE_DIR, '..', 'logs', 'i18m.log')
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

        'mail_admin': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': False,
        },

        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'i18m': {
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
logging.config.dictConfig(LOG_CONFIG)
#################################

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
