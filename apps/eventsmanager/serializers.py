from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import HistoricalEvent


class HistoricalEventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HistoricalEvent
        fields = ('title', 'description', 'keywords', 'startEventDate', 'endEventDate', 'detailsURL', 'detailsURL', 'geoLocation', 'relatedVisualisation', 'languageID', 'userID', 'externalResourceID', 'dateAddedToPC', 'dateIssuedByExternalResource', 'dateModified', 'viewsCount')