__author__ = 'fki'

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *


class UnitSerializer(ModelSerializer):
    unit_category = serializers.HyperlinkedRelatedField(view_name='unit-category-detail')

    class Meta:
        model = Unit


class UnitCategorySerializer(ModelSerializer):
    class Meta:
        model = UnitCategory


class PolicyDomainSerializer(ModelSerializer):
    class Meta:
        model = PolicyDomain


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language


class ExternalResourceSerializer(ModelSerializer):
    class Meta:
        model = ExternalResource
