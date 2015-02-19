"""
All Serializers of the Metrics Manager.
"""

__author__ = 'fki'


from rest_framework.serializers import ModelSerializer, SortedDictWithMetadata
from rest_framework.reverse import reverse
from rest_framework import pagination

from apps.common.fields import *
from .models import Metric, RawDataCategory
from .fields import RawDataField, PolicyDomainsField

import logging
log = logging.getLogger(__name__)


class BaseMetricSerializer(ModelSerializer):
    """
    The base serializer of a metric. All metric serializers must be based on it.
    """
    # Remap some field in order to make the names different from the model names
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
        """
        Deserializes the Django model object
        """
        result = SortedDictWithMetadata()
        # Set the self attribute.
        result['self'] = reverse('metric-detail', args=[obj.pk])
        result.update(super(BaseMetricSerializer, self).to_native(obj))
        return result

    class Meta:
        # The serializers is based on the Metric model
        model = Metric

        # Remove the the newly mapped fields.
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
    """
    The serializer for the metric list.
    """
    # No difference to the base serialzer yet
    pass


class PaginatedListMetricSerializer(pagination.PaginationSerializer):
    """
    Special extension of the ListMetricSerializer to support Pagination.
    """
    class Meta:
        object_serializer_class = ListMetricSerializer


class ReadMetricSerializer(BaseMetricSerializer):
    """
    The serializer for viewing a single metric.
    Basically the base serializer plus the raw data field.
    """

    data = RawDataField()


class WriteMetricSerializer(BaseMetricSerializer):
    """
    Serializer for creating a metric.
    """

    policy_domains = PolicyDomainsField(source='policy_domains', required=True)
    # Make raw data required.
    data = RawDataField(required=True)

    def restore_object(self, attrs, instance=None):
        # Set an intermediate variable with the raw data,
        raw_data = attrs['data']
        # Delete the data attribute, otherwise DRF would raise an error, because this field is not defined in the model.
        del attrs['data']
        metric = super(WriteMetricSerializer, self).restore_object(attrs, instance)
        # hand the raw data to the newly created metric.
        metric.rawdata = raw_data

        return metric


class ExtraCategorySerializer(ModelSerializer):
    """
    Generic Serializer for the Extra Categories.
    """
    class Meta:
        model = RawDataCategory


