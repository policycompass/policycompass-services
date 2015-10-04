from django.db import models

#model which represents an event
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    keywords = models.CharField(max_length=200, blank=True)
    startEventDate = models.DateTimeField(blank=True)
    endEventDate = models.DateTimeField(blank=True)
    detailsURL = models.URLField(max_length=500, blank=True)
    geoLocation = models.CharField(max_length=1000, blank=True)
    relatedVisualisation = models.CharField(max_length=200, blank=True)
    languageID = models.IntegerField()
    userID = models.IntegerField()
    scale = models.CharField(max_length=200, blank=True)
    externalResourceID = models.IntegerField(blank=True,default=0)
    dateAddedToPC = models.DateTimeField(auto_now_add=True)
    dateIssuedByExternalResource = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now_add=True)
    viewsCount = models.IntegerField(blank=True)

#model to store the status of data sources
class Extractor(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    valid = models.BooleanField(default=True)