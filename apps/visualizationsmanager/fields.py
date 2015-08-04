"""
Provides custom serializer fields
"""
__author__ = 'mmilaprat'

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from django.core.exceptions import ObjectDoesNotExist

#from apps.metricsmanager.models import Metric
#from apps.common.serviceadapters import metrics as metrics_service_adapter
#from apps.common.serviceadapters import events as events_service_adapter

from .adapter import * 



import datetime


#class MetricsField(serializers.WritableField):
class DatasetsField(serializers.WritableField):

    def field_to_native(self, obj, field_name):        
        #logging.warning('----DatasetsField--')
        #logging.warning(obj)
        #logging.warning(self.source)
        #ids = []
        ids = getattr(obj, self.source).all()
        result = []

        #metrics = MetricsAdapter()
        datasets = DatasetsAdapter()
        
        for i in ids:        
            #logging.warning('--i--')    
            #logging.warning(i.metric_id)
            #logging.warning(i.visualization_query)
            #result.append(metrics.get(i.dataset_id))
            #result.append(i.dataset_id)
            #temporal = metrics.get(i.dataset_id)
            #temporal = metrics.get(i.id)
            temporal = datasets.get(i.id)
            
            #temporal['visualization_query']= i.visualization_query
            #setattr(temporal, 'descHE', i.description)
            result.append(temporal)
        
        return result

    def from_native(self, value):
        if not type(value) is list:
            raise ValidationError("Datasets property is not a list")
        return value
    

class HistoricalEventsField(serializers.WritableField):

    def field_to_native(self, obj, field_name):
        #logging.warning('--HistoricalEventsField--')
        #logging.warning(self.source)
        #ids = []
        ids = getattr(obj, self.source).all()
        result = []
        #historical_events = references.HistoricalEvents()  
        historical_events = HistoricalEventsAdapter()  
                
        for i in ids:
            #temporal = historical_events.get(i.historical_event_id)
            temporal = historical_events.get(i.id)
            #temporal['descriptionHE']= i.description
            #temporal['color']= i.color
            #setattr(temporal, 'descHE', i.description)
            result.append(temporal)
            #result.append(i.historical_event_id)
            #result.append(i.description)
        return result

    def from_native(self, value):
        if not type(value) is list:
            raise ValidationError("Historical event property is not a list")
        return value


class VisualizationTitleField(serializers.WritableField):

    def field_to_native(self, obj, field_name):
        
        #temporal = Visualization.get(obj.visualization)
        result = obj.visualization.title
        return result

    def from_native(self, value):
        if not type(value) is list:
            raise ValidationError("Visualization is not a list")
        return value