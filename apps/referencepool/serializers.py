from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

__author__ = 'fki'


class UnitCategorySerializer(ModelSerializer):
    class Meta:
        model = UnitCategory


class UnitSerializer(ModelSerializer):
    unit_category = serializers.CharField(source='unit_category.title',
                                          read_only=True)

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


class DateFormatSerializer(ModelSerializer):
    class Meta:
        model = DateFormat


class DataClassSerializer(ModelSerializer):
    class Meta:
        model = DataClass


class IndividualSerializer(ModelSerializer):
    data_class = serializers.CharField(source='data_class.title',
                                       read_only=True)

    class Meta:
        model = Individual


class LicenseSerializer(ModelSerializer):
    class Meta:
        model = License
