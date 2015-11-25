"""
Register the models, which are editable in the Admininterface
"""
from django.contrib import admin
from .models import Visualization, VisualizationInDomain

admin.site.register(Visualization)
admin.site.register(VisualizationInDomain)
