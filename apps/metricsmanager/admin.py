from django.contrib import admin
from .models import Unit, UnitCategory, Metric, MetricInDomain, RawData, RawDataCategory, RawDataExtra, RawDataExtraData

admin.site.register(Metric)
admin.site.register(Unit)
admin.site.register(UnitCategory)
admin.site.register(MetricInDomain)
admin.site.register(RawData)
admin.site.register(RawDataExtra)
admin.site.register(RawDataCategory)
admin.site.register(RawDataExtraData)


