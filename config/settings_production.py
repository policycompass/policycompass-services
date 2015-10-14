"""
Django settings for pc_datamanger project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
from .settings_basic import *
from .settings import *

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    '193.175.133.246',
    'localhost',
]


with open(os.getenv('PC_SECRET_FILE', '/etc/policycompass/secret_key')) as f:
    SECRET_KEY = f.read().strip()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': os.getenv('PC_LOG_LEVEL', 'INFO'),
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': os.getenv('PC_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
    },
}
