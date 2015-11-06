__author__ = 'miquel'
from rest_framework.serializers import ModelSerializer, WritableField, ValidationError, SlugRelatedField, RelatedField, Field
from .models import *
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework import pagination
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from .fields import *

from apps.common.fields import *
from rest_framework.serializers import SortedDictWithMetadata
import datetime
from .fields import DatasetsField, HistoricalEventsField, VisualizationTitleField

import logging
log = logging.getLogger(__name__)


class HistoricalEventSerializer(ModelSerializer):
    class Meta:
        model = HistoricalEventsInVisualizations

class DatasetSerializer(ModelSerializer):
    class Meta:
        model = DatasetsInVisualizations        

class BaseVisualizationLinkedByDatasetSerializer(ModelSerializer):

    title =  VisualizationTitleField(source='visualization')
   
    class Meta:
        model = DatasetsInVisualizations
            
        exclude = (
                   'id',
                   'visualization_query',
            )


class ListVisualizationLinkedByDatasetSerializer(BaseVisualizationLinkedByDatasetSerializer):
    pass


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
    
    creator_path = serializers.Field(source='creator_path')    
    created_at = serializers.DateField(source='created_at', read_only=True)
    updated_at = serializers.DateField(source='updated_at', read_only=True)    
    views_count = serializers.IntegerField(source='views_count')
    visualization_type_id = serializers.IntegerField(source='visualization_type_id')
    status_flag_id = serializers.IntegerField(source='status_flag_id')
    
    historical_events_in_visualization = HistoricalEventsField(source='historical_events_in_visualization', required=False)
    
    datasets_in_visualization = DatasetsField(source='datasets_in_visualization')
    visualization_type_id = serializers.IntegerField(source='visualization_type_id')
    
        
    policy_domains = SlugRelatedField(many=True, slug_field='domain', source='domains')    
    
               
    def to_native(self, obj):     
        result = SortedDictWithMetadata()
        result['self'] = reverse('visualization-detail', args=[obj.pk])
        result.update(super(BaseVisualizationSerializer, self).to_native(obj))
        return result
    

    class Meta:
        model = Visualization


        fields = (
        )


class ListVisualizationSerializer(BaseVisualizationSerializer):
    pass


class PaginatedListDatasetSerializer(pagination.PaginationSerializer):

    class Meta:
        object_serializer_class = ListVisualizationSerializer
        
        
class ReadVisualizationSerializer(BaseVisualizationSerializer):    
    pass


class WriteVisualizationSerializer(BaseVisualizationSerializer):    
    historical_events_in_visualization = HistoricalEventsField(source='historical_events_in_visualization', required=False)   
    datasets_in_visualization = DatasetsField(source='datasets_in_visualization', required=True)   
    
   
    creator_path = serializers.Field(source='creator_path')
    
    policy_domains = WritableField(source='policy_domains')

    def restore_object(self, attrs, instance=None):
        visualization = super(WriteVisualizationSerializer, self).restore_object(attrs, instance)
        return visualization

