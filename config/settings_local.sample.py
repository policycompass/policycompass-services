__author__ = 'fki'

from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'database',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
    }
}