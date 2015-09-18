from django.conf.urls import patterns, url, include

from .api import *

urlpatterns = patterns(
    '',
    url(r'^$', MetricsBase.as_view(), name='metrics-manager-base'),
    url(r'^formula/validate$', FormulaValidate.as_view(), name='metrics-create'),
    url(r'^metrics$', MetricsCreate.as_view(), name='metrics-create'),
    url(r'^metrics/(?P<pk>\d+)$', MetricsDetail.as_view(), name='metrics-detail'),
    url(r'^metrics/(?P<pk>\d+)/operationalize$', MetricsDetail.as_view(), name='metrics-operationalize')
)
