from django.conf.urls import patterns, url, include

from .api import MetricList, MetricDetail, Base, Converter

metric_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', MetricDetail.as_view(), name='metric-detail'),
    url(r'^$', MetricList.as_view(), name='metric-list')
)

converter_urls = patterns(
    '',
    url(r'^$', Converter.as_view(), name='converter')

)

urlpatterns = patterns(
    '',
    url(r'^metrics', include(metric_urls)),
    url(r'^converter', include(converter_urls)),
    url(r'^', Base.as_view(), name="metrics-manager-base")
)