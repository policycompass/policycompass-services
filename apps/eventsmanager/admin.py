from django.contrib import admin
from .models import Event, Extractor


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'keywords', 'startEventDate', 'endEventDate', 'detailsURL', 'detailsURL', 'geoLocation', 'relatedVisualisation', 'languageID', 'userID', 'scale', 'externalResourceID', 'dateAddedToPC', 'dateIssuedByExternalResource', 'dateModified', 'viewsCount')

class ExtractorAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'valid')

admin.site.register(Event, EventAdmin)
admin.site.register(Extractor, ExtractorAdmin)