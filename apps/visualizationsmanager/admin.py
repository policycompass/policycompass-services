"""
Register the models, which are editable in the Admininterface
"""

from django.contrib import admin
from .models import Visualization

admin.site.register(Visualization)


