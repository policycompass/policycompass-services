"""
Provides custom serializer fields
"""
__author__ = 'fki'

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from django.core.exceptions import ObjectDoesNotExist

from apps.common.serviceadapters import references
from .models import RawDataCategory
from .utils import get_rawdata_for_metric

import datetime


class PolicyDomainsField(serializers.WritableField):
    """
    Field for resolving a Policy Domain field.
    The Field must hold a list of integer values, which represent IDs
    """
    def field_to_native(self, obj, field_name):
        """
        Resolves the list of IDs into full representations
        """
        ids = getattr(obj, self.source).all()
        result = []
        # Use the common service adapter
        domains = references.PolicyDomain()
        for i in ids:
            result.append(domains.get(i.domain_id))
        return result

    def from_native(self, value):
        """
        Checks, if the value is a list
        """
        if not type(value) is list:
            raise ValidationError("Policy_domains property is not a list")
        return value


class RawDataField(serializers.WritableField):
    """
    Field for handling the serialization and deserialization of the raw data of a metric.
    """
    def field_to_native(self, obj, field_name):
        """
        Returns the representation of the raw data
        """
        # Process Query Paramters
        params = self.context['request'].QUERY_PARAMS
        order = None
        new_sort = []
        # Get the sort query parameter
        if params.get('sort'):
            sort = params.get('sort')
            # Determine the order
            if sort[:1] == '-':
                order = 'desc'
                sort = sort[1:]

            # Transform the string input into a list
            sort = sort.split(',')
            for s in sort:
                # Some names have to be converted, to match the model name
                if s == 'from':
                    new_sort.append('from_date')
                elif s == 'to':
                    new_sort.append('to_date')
                else:
                    new_sort.append(s)

        # Process the filter parameter for the raw data
        filter = {}
        for p in params:
            # SOme names are reserved
            if p not in ['sort','format']:
                value_list = params.get(p).split(',')
                # Some names have to be converted, to match the model name
                if p == 'from':
                    filter['from_date'] = value_list
                elif p == 'to':
                    filter['to_date'] = value_list
                else:
                    filter[p] = value_list

        # Get the actual raw data and return it
        return get_rawdata_for_metric(obj, sort=new_sort, order=order, filter=filter)

    def from_native(self, value):
        """
        Validates the input of raw data
        """
        # It has to be a dictionary
        if not type(value) is dict:
            raise ValidationError("Wrong datatype")

        # It has to have a table attribute
        if not 'table' in value:
            raise ValidationError("No key table in data")

        # It has to have an extra_columns attribute
        if not 'extra_columns' in value:
            raise ValidationError("No key extra_columns in data")

        # Table has to be a list
        if not type(value['table']) is list:
            raise ValidationError("Table property is not a list")

        # Extra_columns have to a list
        if not type(value['extra_columns']) is list:
            raise ValidationError("Extra Columns property is not a list")

        # The extra columns must be a valid category
        for e in value['extra_columns']:
            try:
                RawDataCategory.objects.get(title=e)
            except ObjectDoesNotExist:
                raise ValidationError("Invalid Extra Column")

        # The table has to have certain properties it its objects
        required_fields = ["to", "from", "value"] + value['extra_columns']
        for r in value['table']:
            if not type(r) is dict:
                raise ValidationError("Table Dict is malformed")

            if not all(k in r for k in required_fields):
                raise ValidationError("Table Dict is malformed, some keys are missing")

            # The date format has to be correct
            try:
                datetime.datetime.strptime(r['from'], '%Y-%m-%d')
            except ValueError:
                raise ValidationError("Wrong Date Format")

            try:
                datetime.datetime.strptime(r['to'], '%Y-%m-%d')
            except ValueError:
                raise ValidationError("Wrong Date Format")

            # The value has to be a float
            try:
                float(r['value'])
            except ValueError:
                raise ValidationError("At least one value is not a float")

        return value

    def validate(self, value):
        pass

