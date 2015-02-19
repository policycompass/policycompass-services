"""
Defines all routes if the Metrics Manager
"""

from django.conf.urls import patterns, url, include

from .api import *

metric_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', MetricDetail.as_view(), name='metric-detail'),
    url(r'^$', MetricList.as_view(), name='metric-list')
)

converter_urls = patterns(
    '',
    url(r'^$', Converter.as_view(), name='converter')

)

categories_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', ExtraCategoryDetail.as_view(), name='extra-detail'),
    url(r'^$', ExtraCategoryList.as_view(), name='extra-list')
)

schema_urls = patterns(
    '',
    url(r'^/(?P<name>\w+)$', SchemasView.as_view(), name='schema-detail'),
)


urlpatterns = patterns(
    '',
    url(r'^metrics', include(metric_urls)),
    url(r'^converter', include(converter_urls)),
    url(r'^extra_categories', include(categories_urls)),
    url(r'^schemas', include(schema_urls)),
    url(r'^', Base.as_view(), name="metrics-manager-base")
)