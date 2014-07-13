from django.conf.urls import patterns, url, include

from .api import MetricList, MetricDetail, UnitList, UnitDetail, Base

unit_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', UnitDetail.as_view(), name='unit-detail'),
    url(r'^$', UnitList.as_view(), name='unit-list')
)

metric_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', MetricDetail.as_view(), name='metric-detail'),
    url(r'^$', MetricList.as_view(), name='metric-list')
)

urlpatterns = patterns(
    '',
    url(r'^metrics', include(metric_urls)),
    url(r'^units', include(unit_urls)),
    url(r'^', Base.as_view(), name="metrics-manager-base")
)