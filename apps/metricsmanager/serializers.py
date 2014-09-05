__author__ = 'fki'

from .models import Metric, RawDataCategory
from rest_framework.serializers import ModelSerializer, SortedDictWithMetadata
from rest_framework.reverse import reverse
from rest_framework import pagination
from apps.common.fields import *
from .fields import RawDataField, PolicyDomainsField

import logging
log = logging.getLogger(__name__)


class BaseMetricSerializer(ModelSerializer):
    spatial = serializers.CharField(source='geo_location', required=False)
    resource_url = serializers.URLField(source='details_url', required=False)
    unit = UnitField(source='unit_id')
    language = LanguageField(source='language_id')
    external_resource = ExternalResourceField(source='ext_resource_id', required=False)
    resource_issued = serializers.DateField(source='publisher_issued', required=False)
    issued = serializers.DateField(source='created_at', read_only=True)
    modified = serializers.DateField(source='updated_at', read_only=True)
    policy_domains = PolicyDomainsField(source='policy_domains')

    def to_native(self, obj):
        result = SortedDictWithMetadata()
        result['self'] = reverse('metric-detail', args=[obj.pk])
        result.update(super(BaseMetricSerializer, self).to_native(obj))
        return result

    class Meta:
        model = Metric

        exclude = (
            'geo_location',
            'details_url',
            'unit_id',
            'language_id',
            'ext_resource_id',
            'publisher_issued',
            'created_at',
            'updated_at'
        )

        fields = (

        )


class ListMetricSerializer(BaseMetricSerializer):
    pass


class PaginatedListMetricSerializer(pagination.PaginationSerializer):

    class Meta:
        object_serializer_class = ListMetricSerializer


class ReadMetricSerializer(BaseMetricSerializer):

    data = RawDataField()


class WriteMetricSerializer(BaseMetricSerializer):

    policy_domains = PolicyDomainsField(source='policy_domains', required=True)
    data = RawDataField(required=True)

    def restore_object(self, attrs, instance=None):
        log.info('Write Metric')
        raw_data = attrs['data']
        del attrs['data']
        metric = super(WriteMetricSerializer, self).restore_object(attrs, instance)
        metric.rawdata = raw_data

        return metric


class ExtraCategorySerializer(ModelSerializer):
    class Meta:
        model = RawDataCategory


