from rest_framework.serializers import ModelSerializer, CharField
from .models import *
from .formula import validate_formula


class MetricSerializer(ModelSerializer):

    formula = CharField(validators=[ validate_formula ])

    class Meta:
        model = Metric
