"""
URLS for the search manager
"""
from django.conf.urls import patterns, url, include
from apps.searchmanager import views
from .api import *

urlpatterns = patterns('',
    url(r'^rebuildindex$', views.rebuildindex_service, name='rebuildindex'),
    url(r'^', Base.as_view(), name="searchmanager-base")
)

