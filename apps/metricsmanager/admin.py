"""
Register the models, which are editable in the Admininterface
"""

from django.contrib import admin
from .models import Metric, MetricInDomain, RawData, RawDataCategory, RawDataExtra, RawDataExtraData

admin.site.register(Metric)
admin.site.register(MetricInDomain)
admin.site.register(RawData)
admin.site.register(RawDataExtra)
admin.site.register(RawDataCategory)
admin.site.register(RawDataExtraData)


