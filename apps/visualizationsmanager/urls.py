from django.conf.urls import patterns, url, include

from .api import VisualizationList, VisualizationDetail, Base

visualization_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', MetricDetail.as_view(), name='visualizations-detail'),
    url(r'^$', VisualizationList.as_view(), name='visualizations-list')
)

urlpatterns = patterns(
    '',
    url(r'^visualizations', include(visualization_urls)),
    url(r'^', Base.as_view(), name="isualizations-manager-base")
)