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


class MetricsField(serializers.WritableField):

    def field_to_native(self, obj, field_name):        
        #logging.warning('----MetricsField--')
        #logging.warning(obj)
        #logging.warning(self.source)
        #ids = []
        ids = getattr(obj, self.source).all()
        result = []
        #metrics = references.Metrics()
        metrics = MetricsAdapter()
        
        
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
        #historical_events = references.HistoricalEvents()  
        historical_events = HistoricalEventsAdapter()  
                
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
