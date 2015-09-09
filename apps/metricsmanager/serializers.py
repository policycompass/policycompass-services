from rest_framework.serializers import ModelSerializer
from .models import *


class MetricSerializer(ModelSerializer):
    class Meta:
        model = Metric
