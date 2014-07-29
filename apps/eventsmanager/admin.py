from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'keywords', 'startEventDate', 'endEventDate', 'detailsURL', 'detailsURL', 'geoLocation', 'relatedVisualisation', 'languageID', 'userID', 'externalResourceID', 'dateAddedToPC', 'dateIssuedByExternalResource', 'dateModified', 'viewsCount')


admin.site.register(Event, EventAdmin)