"""
Defines all routes of the Event Manager
"""

from django.conf.urls import patterns, url
from apps.eventsmanager import views
from .views import *

urlpatterns = patterns('',
                       url(r'^events$', views.EventView.as_view(), name='author-list'),
                       url(r'^events/(?P<pk>[\d]+)$', views.EventInstanceView.as_view(), name='event-instance'),
                       url(r'^harvestevents$', views.HarvestEvents.as_view(), name='harvest-events'),
                       url(r'^configextractor$', views.ConfigExtractor.as_view(), name='config-extractor'),
                       url(r'^getextractor$', views.GetExtractor.as_view(), name='get-extractor'),
                       url(r'^', Base.as_view(), name="event-base")
                       )
