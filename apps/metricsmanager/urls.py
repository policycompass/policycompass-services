from django.conf.urls import patterns, url, include

from .api import MetricList, MetricDetail, Base, Converter, ExtraCategoryList, ExtraCategoryDetail

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

urlpatterns = patterns(
    '',
    url(r'^metrics', include(metric_urls)),
    url(r'^converter', include(converter_urls)),
    url(r'^extra_categories', include(categories_urls)),
    url(r'^', Base.as_view(), name="metrics-manager-base")
)