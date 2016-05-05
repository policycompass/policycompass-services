"""
Register the models, which are editable in the Admininterface
"""
from django.contrib import admin
from .models import Visualization, VisualizationInDomain, HistoricalEventsInVisualizations, DatasetsInVisualizations

admin.site.register(Visualization)
admin.site.register(VisualizationInDomain)
admin.site.register(HistoricalEventsInVisualizations)
admin.site.register(DatasetsInVisualizations)
