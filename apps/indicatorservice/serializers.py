__author__ = 'fki'

from rest_framework.serializers import ModelSerializer, WritableField
from rest_framework import serializers
from rest_framework import pagination
from .models import *


class IndicatorSerializer(ModelSerializer):
    policy_domains = serializers.SlugRelatedField(many=True, slug_field='domain', source='domains')
    creator_path = serializers.Field(source='creator_path')

    class Meta:
        model = Indicator


class CreateIndicatorSerializer(IndicatorSerializer):
    policy_domains = WritableField(source='policy_domains', required=True)

    class Meta:
        model = Indicator


class PaginatedListIndicatorSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = IndicatorSerializer
