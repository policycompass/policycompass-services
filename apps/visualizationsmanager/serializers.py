__author__ = 'miquel'

from .models import Metric, Visualization, MetricsInVisualizations, HistoricalEventsInVisualizations
#,  RawDataCategory
from rest_framework.serializers import ModelSerializer, WritableField, ValidationError
from rest_framework import serializers
#from .utils import get_rawdata_for_visualization
from rest_framework.reverse import reverse
from rest_framework import pagination
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
#from apps.common.serviceadapters import references
from apps.common.fields import *
from rest_framework.serializers import SortedDictWithMetadata
import datetime

import logging
log = logging.getLogger(__name__)

        
class MetricsField(serializers.WritableField):

    def field_to_native(self, obj, field_name):        
        #logging.warning('----MetricsField--')
        #logging.warning(obj)
        #logging.warning(self.source)
        #ids = []
        ids = getattr(obj, self.source).all()
        result = []
        metrics = references.Metrics()  
        #metrics = references.PolicyDomain()     
        for i in ids:        
            #logging.warning('--i--')    
            #logging.warning(i.metric_id)
            #logging.warning(i.visualization_query)
            #result.append(metrics.get(i.metric_id))
            #result.append(i.metric_id)
            temporal = metrics.get(i.metric_id)
            temporal['visualization_query']= i.visualization_query
            #setattr(temporal, 'descHE', i.description)
            result.append(temporal)

            
        return result

    def from_native(self, value):
        if not type(value) is list:
            raise ValidationError("Metrics property is not a list")
        return value
    
  
        
class HistoricalEventsField(serializers.WritableField):

    def field_to_native(self, obj, field_name):
        #logging.warning('--HistoricalEventsField--')
        #logging.warning(self.source)
        #ids = []
        ids = getattr(obj, self.source).all()
        result = []
        historical_events = references.HistoricalEvents()       
        for i in ids:
            temporal = historical_events.get(i.historical_event_id)
            temporal['descriptionHE']= i.description
            #setattr(temporal, 'descHE', i.description)
            result.append(temporal)
            #result.append(i.historical_event_id)
            #result.append(i.description)
        return result

    def from_native(self, value):
        if not type(value) is list:
            raise ValidationError("Historical event property is not a list")
        return value
    
    



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
    

#    def to_native(self, obj):
#        result = super(BaseVisualizationSerializer, self).to_native(obj)
#        result['self'] = reverse('visualization-detail', args=[obj.pk], request=self.context['request'])
#        return result

    def to_native(self, obj):
        result = SortedDictWithMetadata()
        result['self'] = reverse('visualization-detail', args=[obj.pk])
        result.update(super(BaseVisualizationSerializer, self).to_native(obj))
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

class PaginatedListMetricSerializer(pagination.PaginationSerializer):

    class Meta:
        object_serializer_class = ListVisualizationSerializer
        
        
class ReadVisualizationSerializer(BaseVisualizationSerializer):
    pass
    #data = RawDataField()


class WriteVisualizationSerializer(BaseVisualizationSerializer):

    historical_events_in_visualization = HistoricalEventsField(source='historical_events_in_visualization', required=False)
    metrics_in_visualization = MetricsField(source='metrics_in_visualization', required=False)
    #data = RawDataField(required=True, write_only=True)

    def restore_object(self, attrs, instance=None):

        #raw_data = attrs['data']
        #del attrs['data']
        visualization = super(WriteVisualizationSerializer, self).restore_object(attrs, instance)
        #visualization.rawdata = raw_data

        return visualization

