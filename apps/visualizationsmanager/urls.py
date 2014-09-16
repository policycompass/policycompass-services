from django.conf.urls import patterns, url, include

#from .api import VisualizationList, VisualizationDetail, Base
from .api import *

visualization_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', VisualizationDetail.as_view(), name='visualization-detail'),
    url(r'^$', VisualizationList.as_view(), name='visualization-list')
)

visualization_metrics_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', MetricDetailForVisualization.as_view(), name='metric-detail-for-visualization'),
    url(r'^$', MetricListForVisualization.as_view(), name='metric-list-for-visualization')
)

visualization_events_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', EventDetailForVisualization.as_view(), name='event-detail-for-visualization'),
    url(r'^$', EventListForVisualization.as_view(), name='event-list-for-visualization')
)


urlpatterns = patterns(
    '',
    url(r'^visualizations', include(visualization_urls)),
    url(r'^metricsInVisualizations', include(visualization_metrics_urls)),
    url(r'^eventsInVisualizations', include(visualization_events_urls)),    
    url(r'^', Base.as_view(), name="visualizations-manager-base")
)