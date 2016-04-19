from django.contrib import admin
from .models import *


admin.site.register(Event)
admin.site.register(EventInDomain)
admin.site.register(EventInSpatial)
admin.site.register(Extractor)
