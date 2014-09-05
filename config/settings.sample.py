__author__ = 'fki'

from .settings_basic import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'pcompass.db',
    }
}

# Database config example for PostgreSQL

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'pcompass',
#         'USER': 'pcompass',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#     }
# }



PC_SERVICES = {
    'references': {
        'base_url': 'http://localhost:8000',
        'units': '/api/v1/references/units',
        'external_resources': '/api/v1/references/externalresources',
        'languages': '/api/v1/references/languages',
        'domains': '/api/v1/references/policydomains',
        'events': '/api/v1/references/events',
        'metrics': '/api/v1/references/metrics'        
    }
}
