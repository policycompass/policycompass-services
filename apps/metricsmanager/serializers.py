from rest_framework import serializers
from .models import *
from .formula import validate_formula
from drf_compound_fields import fields as compound_fields

class MetricSerializer(serializers.ModelSerializer):

    formula = serializers.CharField(validators=[ validate_formula ])

    class Meta:
        model = Metric

class OperationalizeMappingSerializer(serializers.Serializer):
    variable = serializers.RegexField("__[0-9]+__")
    dataset = serializers.IntegerField(min_value=0)

    def restore_object(self, validated_data, instance=None):
        return (validated_data['variable'], validated_data['dataset'])

class OperationalizeSerializer(serializers.Serializer):
    datasets = compound_fields.ListField(OperationalizeMappingSerializer())

    def restore_object(self, validated_data, instance=None):
        return dict(validated_data['datasets'])
