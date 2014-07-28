from django.contrib import admin
from .models import Visualization, RawData, RawDataCategory, RawDataExtra, RawDataExtraData

admin.site.register(Visualization)
admin.site.register(RawData)
admin.site.register(RawDataExtra)
admin.site.register(RawDataCategory)
admin.site.register(RawDataExtraData)


