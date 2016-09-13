from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework import pagination
from .models import *

__author__ = 'fki'


class IndicatorSerializer(ModelSerializer):
    creator_path = serializers.Field(source='creator_path')

    class Meta:
        model = Indicator


class CreateIndicatorSerializer(IndicatorSerializer):

    class Meta:
        model = Indicator


class PaginatedListIndicatorSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = IndicatorSerializer
