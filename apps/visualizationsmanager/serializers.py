__author__ = 'miquel'

from .models import Visualization,  RawDataCategory
from rest_framework.serializers import ModelSerializer, WritableField, ValidationError
from rest_framework import serializers
from .utils import get_rawdata_for_visualization
from rest_framework.reverse import reverse
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from apps.common.serviceadapters import references
from apps.common.fields import *

import datetime

import logging
log = logging.getLogger(__name__)

        
        
class MetricsField(serializers.WritableField):

    def field_to_native(self, obj, field_name):
        #ids = getattr(obj, self.source).all()        
        ids = []
        result = []
        metrics_list = references.Metrics()       
        for i in ids:            
            #result.append(metrics_list.get(i.metric_id))
            result.append(1)
        return result

    def from_native(self, value):
        if not type(value) is list:
            raise ValidationError("Metrics property is not a list")
        return value
    
  
        
class HistoricalEventsField(serializers.WritableField):

    def field_to_native(self, obj, field_name):
        #ids = getattr(obj, self.source).all()
        ids = []
        result = []
        historical_events = references.HistoricalEvents()       
        for i in ids:
            #result.append(domains.get(i.domain_id))
            result.append(1)
        return result

    def from_native(self, value):
        if not type(value) is list:
            raise ValidationError("Historical event property is not a list")
        return value
    
    

class RawDataField(serializers.WritableField):
    def field_to_native(self, obj, field_name):
        return get_rawdata_for_visualization(obj)

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


class BaseVisualizationSerializer(ModelSerializer):
    #spatial = serializers.CharField(source='geo_location', blank=True)
    #resource_url = serializers.URLField(source='details_url', blank=True)
    #unit = UnitField(source='unit_id')
    language = LanguageField(source='language_id')
    #external_resource = ExternalResourceField(source='ext_resource_id', blank=True)
    ##resource_issued = serializers.DateField(source='publisher_issued', blank=True)
    created_at = serializers.DateField(source='created_at', read_only=True)
    updated_at = serializers.DateField(source='updated_at', read_only=True)
    
    views_count = serializers.IntegerField(source='views_count')
    visualization_type_id = serializers.IntegerField(source='visualization_type_id')
    status_flag_id = serializers.IntegerField(source='status_flag_id')
    
    historical_events_in_visualization = HistoricalEventsField(source='historical_events_in_visualization')
    metrics_in_visualization = MetricsField(source='metrics_in_visualization')
    #historical_events_in_visualization = HistoricalEventsField(source='historical_events')
    

    def to_native(self, obj):
        result = super(BaseVisualizationSerializer, self).to_native(obj)
        result['self'] = reverse('visualization-detail', args=[obj.pk], request=self.context['request'])
        return result

    class Meta:
        model = Visualization

        exclude = (
            'language_id',
            #'publisher_issued',
            #'created_at',
            'updated_at'
            #'historical_events_in_visualization'
        )

        fields = (
        )


class ListVisualizationSerializer(BaseVisualizationSerializer):
    pass


class ReadVisualizationSerializer(BaseVisualizationSerializer):

    data = RawDataField()


class WriteVisualizationSerializer(BaseVisualizationSerializer):

    historical_events_in_visualization = HistoricalEventsField(source='historical_events_in_visualization', required=False)
    metrics_in_visualization = MetricsField(source='metrics_in_visualization', required=False)
    data = RawDataField(required=True, write_only=True)

    def restore_object(self, attrs, instance=None):

        raw_data = attrs['data']
        del attrs['data']
        visualization = super(WriteVisualizationSerializer, self).restore_object(attrs, instance)
        visualization.rawdata = raw_data

        return visualization

