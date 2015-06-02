__author__ = 'fki'

from rest_framework.serializers import ModelSerializer
from .models import *


class DatasetSerializer(ModelSerializer):
    class Meta:
        model = Dataset


