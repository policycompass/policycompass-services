__author__ = 'fki'

from .models import Metric, RawDataCategory
from rest_framework.serializers import ModelSerializer, WritableField, ValidationError
from rest_framework import serializers
from .utils import get_rawdata_for_metric
from rest_framework.reverse import reverse
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
import datetime

import logging
log = logging.getLogger(__name__)


class RawDataField(serializers.WritableField):
    def field_to_native(self, obj, field_name):
        return get_rawdata_for_metric(obj)

    def from_native(self, value):
        if not type(value) is dict:
            raise ValidationError("Wrong datatype")

        if not 'table' in value:
            raise ValidationError("No key table in data")

        if not 'extra_columns' in value:
            raise ValidationError("No key extra_columns in data")

        if not type(value['table']) is list:
            raise ValidationError("Table property is not a list")

        if not type(value['extra_columns']) is list:
            raise ValidationError("Extra Columns property is not a list")

        for e in value['extra_columns']:
            try:
                RawDataCategory.objects.get(title=e)
            except ObjectDoesNotExist:
                raise ValidationError("Invalid Extra Column")

        required_fields = ["to", "from", "value"] + value['extra_columns']
        for r in value['table']:
            if not type(r) is dict:
                raise ValidationError("Table Dict is malformed")

            if not all(k in r for k in required_fields):
                raise ValidationError("Table Dict is malformed, some keys are missing")

            try:
                datetime.datetime.strptime(r['from'], '%Y-%m-%d')
            except ValueError:
                raise ValidationError("Wrong Date Format")

            try:
                datetime.datetime.strptime(r['to'], '%Y-%m-%d')
            except ValueError:
                raise ValidationError("Wrong Date Format")

            try:
                float(r['value'])
            except ValueError:
                raise ValidationError("At least one value is not a float")


        return value

    def validate(self, value):
        pass


class BaseMetricSerializer(ModelSerializer):
    spatial = serializers.CharField(source='geo_location', blank=True)
    resource_url = serializers.URLField(source='details_url', blank=True)
    unit = serializers.IntegerField(source='unit_id')
    language = serializers.IntegerField(source='language_id')
    external_resource = serializers.IntegerField(source='ext_resource_id', blank=True)
    resource_issued = serializers.DateField(source='publisher_issued', blank=True)
    issued = serializers.DateField(source='created_at', read_only=True)
    modified = serializers.DateField(source='updated_at', read_only=True)

    def to_native(self, obj):
        result = super(BaseMetricSerializer, self).to_native(obj)
        result['self'] = reverse('metric-detail', args=[obj.pk], request=self.context['request'])
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


class ReadMetricSerializer(BaseMetricSerializer):

    data = RawDataField()


class WriteMetricSerializer(BaseMetricSerializer):

    data = RawDataField(required=True, write_only=True)

    def restore_object(self, attrs, instance=None):

        raw_data = attrs['data']
        del attrs['data']
        metric = super(WriteMetricSerializer, self).restore_object(attrs, instance)
        metric.rawdata = raw_data

        return metric

