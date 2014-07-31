from django.conf.urls import patterns, url, include

from .api import VisualizationList, VisualizationDetail, Base

visualization_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', VisualizationDetail.as_view(), name='visualization-detail'),
    url(r'^$', VisualizationList.as_view(), name='visualization-list')
)

urlpatterns = patterns(
    '',
    url(r'^visualizations', include(visualization_urls)),
    url(r'^', Base.as_view(), name="visualizations-manager-base")
)