__author__ = 'fki'

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework import pagination
from .models import *


class IndicatorSerializer(ModelSerializer):
    policy_domains = serializers.SlugRelatedField(many=True, slug_field='domain')

    class Meta:
        model = Indicator


class PaginatedListIndicatorSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = IndicatorSerializer
