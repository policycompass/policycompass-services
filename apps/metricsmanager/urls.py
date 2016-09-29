from django.conf.urls import patterns, url
from .api import *

urlpatterns = patterns(
    '',
    url(r'^$', MetricsBase.as_view(), name='metrics-manager-base'),
    url(r'^formulas/validate$', FormulasValidate.as_view(), name='formulas-validate'),
    url(r'^normalizers$', NormalizersList.as_view(), name='normalizers-list'),
    url(r'^calculate', DatasetCalculateView.as_view(), name='calculate-dataset'),
    url(r'^metrics$', MetricsCreate.as_view(), name='metrics-create-list'),
    url(r'^metrics/(?P<pk>\d+)$', MetricsDetail.as_view(), name='metrics-detail'),
    url(r'^metrics/(?P<metrics_id>\d+)/operationalize$', MetriscOperationalize.as_view(), name='metrics-operationalize')
)
