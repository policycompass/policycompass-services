from django.db import models


class HistoricalEvent(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    keywords = models.CharField(max_length=200, blank=True)
    startEventDate = models.DateTimeField(blank=True)
    endEventDate = models.DateTimeField(blank=True)
    detailsURL = models.CharField(max_length=200, blank=True)
    geoLocation = models.CharField(max_length=200, blank=True)
    relatedVisualisation = models.CharField(max_length=200, blank=True)
    languageID = models.CharField(max_length=200, blank=True)
    userID = models.CharField(max_length=200, blank=True)
    externalResourceID = models.CharField(max_length=200, blank=True)
    dateAddedToPC = models.DateTimeField(blank=True)
    dateIssuedByExternalResource = models.DateTimeField(blank=True)
    dateModified = models.DateTimeField(blank=True)
    viewsCount = models.IntegerField(blank=True)