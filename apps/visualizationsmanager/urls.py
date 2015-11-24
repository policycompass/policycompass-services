from django.conf.urls import patterns, url, include
from .api import *

visualization_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', VisualizationDetail.as_view(),
        name='visualization-detail'),
    url(r'^$', VisualizationList.as_view(), name='visualization-list')
)

visualization_datasets_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', DatasetDetailForVisualization.as_view(),
        name='dataset-detail-for-visualization'),
    url(r'^$', DatasetListForVisualization.as_view(),
        name='dataset-list-for-visualization')
)

visualization_events_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', EventDetailForVisualization.as_view(),
        name='event-detail-for-visualization'),
    url(r'^$', EventListForVisualization.as_view(),
        name='event-list-for-visualization')
)

visualizations_linked_with_dataset = patterns(
    '',
    url(r'^$', VisualizationsLinkedByDataset.as_view(),
        name='linked-visualizations-by-dataset')
)

visualizations_linked_with_event = patterns(
    '',
    url(r'^$', VisualizationsLinkedByEvent.as_view(),
        name='linked-visualizations-by-event')
)

urlpatterns = patterns(
    '',
    url(r'^visualizations', include(visualization_urls)),
    url(r'^datasetsInVisualizations', include(visualization_datasets_urls)),
    url(r'^eventsInVisualizations', include(visualization_events_urls)),
    url(r'^linkedVisualizationsByDataset',
        include(visualizations_linked_with_dataset)),
    url(r'^linkedVisualizationsByEvent',
        include(visualizations_linked_with_event)),
    url(r'^', Base.as_view(), name="visualizations-manager-base")
)
