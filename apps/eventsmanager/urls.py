from django.conf.urls import patterns, url
from apps.eventsmanager import views
from .views import *

urlpatterns = patterns('',
     #url(r'^', include(router.urls)),
     url(r'^events$', views.EventView.as_view(), name='author-list'),
     url(r'^events/(?P<pk>[\d]+)$', views.EventInstanceView.as_view(), name='event-instance'),
     url(r'^', Base.as_view(), name="event-base")
)