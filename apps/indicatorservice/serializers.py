__author__ = 'fki'

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
import apps.referencepool.serializers as reference_serializers


class IndicatorSerializer(ModelSerializer):
    class Meta:
        model = Indicator

