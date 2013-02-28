# -*- coding: utf8 -*-
# Django settings for profsoux project.
from profsoux.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Mikhail Baranov', 'dev@brnv.ru'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'data.db'),
    }
}

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'uploads')

MEDIA_URL = 'http://testmedia.profsoux.ru/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

STATIC_URL = 'http://teststatic.profsoux.ru/'

ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
