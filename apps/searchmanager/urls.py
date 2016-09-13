"""
URLS for the search manager
"""
from django.conf.urls import patterns, url
from apps.searchmanager import views
from .api import *

urlpatterns = patterns(
    '',
    url(r'^rebuildindex$', views.rebuildindex_service, name='rebuildindex'),
    url(r'^rebuildindex_metric$', views.rebuildindex_metric_service, name='rebuildindex_metric'),
    url(r'^rebuildindex_event$', views.rebuildindex_event_service, name='rebuildindex_event'),
    url(r'^rebuildindex_dataset$', views.rebuildindex_dataset_service, name='rebuildindex_dataset'),
    url(r'^rebuildindex_indicator$', views.rebuildindex_indicator_service, name='rebuildindex_indicator'),
    url(r'^rebuildindex_fuzzymap$', views.rebuildindex_fuzzymap_service, name='rebuildindex_fuzzymap'),
    url(r'^rebuildindex_visualization$', views.rebuildindex_visualization_service, name='rebuildindex_visualization'),
    url(r'^rebuildindex_story$', views.rebuildindex_story_service, name='rebuildindex_story'),
    url(r'^rebuildindex_ag$', views.rebuildindex_story_service, name='rebuildindex_ag'),
    url(r'^updateindexitem/(?P<itemtype>\w+)/(?P<itemid>\d+)$', views.update_index_item_service, name='update_index_item'),
    url(r'^deleteindexitem/(?P<itemtype>\w+)/(?P<itemid>\d+)$', views.delete_index_item_service, name='delete_index_item'),
    url(r'^', Base.as_view(), name="searchmanager-base")
)
