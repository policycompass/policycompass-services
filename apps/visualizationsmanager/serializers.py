__author__ = 'miquel'

#from .models import Visualization, MetricsInVisualizations, HistoricalEventsInVisualizations
from .models import Visualization, DatasetsInVisualizations, HistoricalEventsInVisualizations
from rest_framework.serializers import ModelSerializer, WritableField, ValidationError
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework import pagination
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
#from apps.metricsmanager.models import Metric
#from apps.eventsmanager.models import Event


from apps.common.fields import *
from rest_framework.serializers import SortedDictWithMetadata
import datetime
#from .fields import MetricsField, HistoricalEventsField, VisualizationTitleField
from .fields import DatasetsField, HistoricalEventsField, VisualizationTitleField

import logging
log = logging.getLogger(__name__)


class HistoricalEventSerializer(ModelSerializer):
    class Meta:
        #model = Event
        model = HistoricalEventsInVisualizations

       
#class MetricSerializer(ModelSerializer):
#    class Meta:
#        #model = Metric
#        model = MetricsInVisualizations
        
class DatasetSerializer(ModelSerializer):
    class Meta:
        model = DatasetsInVisualizations        

#class BaseVisualizationLinkedByMetricSerializer(ModelSerializer):
#
#    title =  VisualizationTitleField(source='visualization')
#   
#    class Meta:
#        model = MetricsInVisualizations
#            
#        exclude = (
#                   'id',
#                   'visualization_query',
#            )

class BaseVisualizationLinkedByDatasetSerializer(ModelSerializer):

    title =  VisualizationTitleField(source='visualization')
   
    class Meta:
        model = DatasetsInVisualizations
            
        exclude = (
                   'id',
                   'visualization_query',
            )

#class ListVisualizationLinkedByMetricSerializer(BaseVisualizationLinkedByMetricSerializer):
#    pass

class ListVisualizationLinkedByDatasetSerializer(BaseVisualizationLinkedByDatasetSerializer):
    pass

#class PaginatedListVisualizationLinkedByMetricSerializer(pagination.PaginationSerializer):    
#    class Meta:
#        object_serializer_class = ListVisualizationLinkedByMetricSerializer

class PaginatedListVisualizationLinkedByDatasetSerializer(pagination.PaginationSerializer):    
    class Meta:
        object_serializer_class = ListVisualizationLinkedByDatasetSerializer


class BaseVisualizationLinkedByEventSerializer(ModelSerializer):

    title =  VisualizationTitleField(source='visualization')
   
    class Meta:
        
        model =  HistoricalEventsInVisualizations
            
        exclude = (
                   'id',
                   'description',
                   'color',
            )
        
class ListVisualizationLinkedByEventSerializer(BaseVisualizationLinkedByEventSerializer):
    pass

class PaginatedListVisualizationLinkedByEventSerializer(pagination.PaginationSerializer):    
    class Meta:
        object_serializer_class = ListVisualizationLinkedByEventSerializer
        
class BaseVisualizationSerializer(ModelSerializer):
    #spatial = serializers.CharField(source='geo_location', blank=True)
    #resource_url = serializers.URLField(source='details_url', blank=True)
    #unit = UnitField(source='unit_id')
    #language = LanguageField(source='language_id')
    
    
    #external_resource = ExternalResourceField(source='ext_resource_id', blank=True)
    ##resource_issued = serializers.DateField(source='publisher_issued', blank=True)
    created_at = serializers.DateField(source='created_at', read_only=True)
    updated_at = serializers.DateField(source='updated_at', read_only=True)
    
    views_count = serializers.IntegerField(source='views_count')
    visualization_type_id = serializers.IntegerField(source='visualization_type_id')
    status_flag_id = serializers.IntegerField(source='status_flag_id')
    
    historical_events_in_visualization = HistoricalEventsField(source='historical_events_in_visualization')
    #metrics_in_visualization = MetricsField(source='metrics_in_visualization')
    
    datasets_in_visualization = DatasetsField(source='datasets_in_visualization')
    
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

#        exclude = (
#            'language_id',
#            #'publisher_issued',
#            #'created_at',
#            'updated_at'
#            #'historical_events_in_visualization'
#        )

        fields = (
        )


class ListVisualizationSerializer(BaseVisualizationSerializer):
    pass

#class PaginatedListMetricSerializer(pagination.PaginationSerializer):
#
#    class Meta:
#        object_serializer_class = ListVisualizationSerializer

class PaginatedListDatasetSerializer(pagination.PaginationSerializer):

    class Meta:
        object_serializer_class = ListVisualizationSerializer
        
        
class ReadVisualizationSerializer(BaseVisualizationSerializer):
    pass
    #data = RawDataField()


class WriteVisualizationSerializer(BaseVisualizationSerializer):

    historical_events_in_visualization = HistoricalEventsField(source='historical_events_in_visualization', required=False)
    #metrics_in_visualization = MetricsField(source='metrics_in_visualization', required=False)
    datasets_in_visualization = DatasetsField(source='datasets_in_visualization', required=False)
    
    #data = RawDataField(required=True, write_only=True)

    def restore_object(self, attrs, instance=None):

        #raw_data = attrs['data']
        #del attrs['data']
        visualization = super(WriteVisualizationSerializer, self).restore_object(attrs, instance)
        #visualization.rawdata = raw_data

        return visualization

