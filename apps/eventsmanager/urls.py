from django.conf.urls import patterns, url
from apps.eventsmanager import views

urlpatterns = patterns('',
     #url(r'^', include(router.urls)),
     url(r'^events$', views.EventView.as_view(), name='author-list'),
     url(r'^events/(?P<pk>[\d]+)$', views.EventInstanceView.as_view(), name='event-instance'),
)