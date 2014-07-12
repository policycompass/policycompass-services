from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(ExternalResource)
admin.site.register(Language)
admin.site.register(PolicyDomain)
admin.site.register(UnitCategory)
admin.site.register(Unit)

