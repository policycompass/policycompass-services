"""
Register the models, which are editable in the Admininterface
"""

from django.contrib import admin
from .models import Metric

admin.site.register(Metric)
