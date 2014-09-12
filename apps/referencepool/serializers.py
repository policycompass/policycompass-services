__author__ = 'fki'

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

from apps.metricsmanager.models import Metric
from apps.eventsmanager.models import Event
from apps.visualizationsmanager.models import HistoricalEventsInVisualizations

class HistoricalEventSerializer(ModelSerializer):
    class Meta:
        model = Event
        
class MetricSerializer(ModelSerializer):
    class Meta:
        model = Metric


class UnitCategorySerializer(ModelSerializer):
    class Meta:
        model = UnitCategory


class UnitSerializer(ModelSerializer):
    unit_category = UnitCategorySerializer()

    class Meta:
        model = Unit


class PolicyDomainSerializer(ModelSerializer):
    class Meta:
        model = PolicyDomain


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language


class ExternalResourceSerializer(ModelSerializer):
    class Meta:
        model = ExternalResource
