# -*- coding: utf-8 -*-
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

MEDIA_URL = 'http://media.profsoux.ru/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'markup')

STATIC_URL = 'http://static.profsoux.ru/'

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
# TinyMCE Settings
TINYMCE_JS_URL = STATIC_URL + 'grappelli/tinymce/jscripts/tiny_mce/'
TINYMCE_JS_ROOT = STATIC_URL + 'js/tiny_mce/'

FILEBROWSER_MEDIA_ROOT = MEDIA_ROOT
FILEBROWSER_DIRECTORY = ''
FILEBROWSER_MEDIA_URL = MEDIA_URL
FILEBROWSER_URL_TINYMCE = TINYMCE_JS_URL
