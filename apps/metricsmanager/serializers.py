from rest_framework import serializers
from .models import *
from .formula import validate_variables, validate_formula
from drf_compound_fields import fields as compound_fields


class MetricSerializer(serializers.ModelSerializer):
    creator_path = serializers.Field(source='creator_path')

    def validate_variables(self, attrs, source):
        """
        Check if the structure of the variables map is as expected and remove
        any additional keys provided.
        """
        attrs['variables'] = validate_variables(attrs['variables'])
        return attrs

    def validate(self, attrs):
        """
        Check formula and that provided mappings cover all variables and filter
        supplementary mappings.
        """
        variables_used = validate_formula(attrs['formula'], attrs['variables'])

        # Accept if too many vars are provided and filter them here
        attrs['variables'] = {var_name: value for var_name, value
                              in attrs['variables'].items()
                              if var_name in variables_used}
        return attrs

    class Meta:
        model = Metric


class OperationalizeMappingSerializer(serializers.Serializer):
    variable = serializers.RegexField("__[0-9]+__")
    dataset = serializers.IntegerField(min_value=0)

    def restore_object(self, validated_data, instance=None):
        return (validated_data['variable'], validated_data['dataset'])


class OperationalizeSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    unit_id = serializers.IntegerField()
    datasets = compound_fields.ListField(OperationalizeMappingSerializer())

    def restore_object(self, validated_data, instance=None):
        validated_data['datasets'] = dict(validated_data['datasets'])
        return validated_data


class CalculateSerializer(OperationalizeSerializer):
    indicator_id = serializers.IntegerField()
    formula = serializers.CharField()


class NormalizerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    acronym = serializers.CharField(max_length=20)
    description = serializers.CharField(max_length=500)
    arguments = serializers.Field(source="get_arguments")
