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

with open('/etc/policycompass/secret_key') as f:
    SECRET_KEY = f.read().strip()
