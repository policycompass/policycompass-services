__author__ = 'fki'

from .settings_basic import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'metricsmanager',
        'USER': 'poco',
        'PASSWORD': '123456',
        'HOST': 'localhost',
    }
}