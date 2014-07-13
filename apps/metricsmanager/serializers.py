__author__ = 'fki'

from .models import Metric, Unit
from rest_framework.serializers import ModelSerializer, WritableField, ValidationError
from rest_framework import serializers
from .utils import get_rawdata_for_metric

import logging
log = logging.getLogger(__name__)


class RawDataField(serializers.WritableField):
    def field_to_native(self, obj, field_name):
        return get_rawdata_for_metric(obj)

    def from_native(self, value):
        if not type(value) is dict:
            raise ValidationError("Wrong datatype")

        l = len(value['value'])

        for key, v in value.iteritems():
            if len(v) != l:
                raise ValidationError("Columns are not aligned")

        return value

    def validate(self, value):
        pass


class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = (
            'id',
            'title',
            'description'
        )


class BaseMetricSerializer(ModelSerializer):
    hallo = serializers.CharField(source='keywords')


    class Meta:
        model = Metric

        fields = (
        )


class ListMetricSerializer(BaseMetricSerializer):
    unit = UnitSerializer()


class ReadMetricSerializer(BaseMetricSerializer):

    data = RawDataField()
    unit = UnitSerializer()


class WriteMetricSerializer(BaseMetricSerializer):

    data = RawDataField(required=True, write_only=True)
    unit = serializers.SlugRelatedField(slug_field='id')

    def restore_object(self, attrs, instance=None):

        raw_data = attrs['data']
        del attrs['data']
        metric = super(WriteMetricSerializer, self).restore_object(attrs, instance)
        metric.rawdata = raw_data

        return metric

