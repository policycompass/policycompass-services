"""
Register the models, which are editable in the Admininterface
"""

from django.contrib import admin
from .models import Dataset, DatasetInDomain

admin.site.register(Dataset)
admin.site.register(DatasetInDomain)
