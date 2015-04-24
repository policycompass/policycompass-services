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

import logging
log = logging.getLogger(__name__)


class PolicyDomainsField(serializers.Field):

    def get_attribute(self, obj):
        """
        Field for resolving a Policy Domain field.
        The Field must hold a list of integer values, which represent IDs
        """
        ids = getattr(obj, self.source).all()
        result = []
        # Use the common service adapter
        domains = references.PolicyDomain()
        for i in ids:
            result.append(domains.get(i.domain_id))
        return result

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        """
        Checks, if the value is a list
        """
        if not type(data) is list:
            raise ValidationError("Policy_domains property is not a list")
        return data


class RawDataField(serializers.Field):
    """
    Field for handling the serialization and deserialization of the raw data of a metric.
    """
    def to_representation(self, value):
        return value

    def get_attribute(self, obj):
        """
        Returns the representation of the raw data
        """
        # Process Query Paramters
        params = self.context['request'].query_params
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

    def to_internal_value(self, value):
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

        date_format = None
        if 'date_format' in value:
            if not type(value['date_format']) is int:
                raise ValidationError("Date Format is not an Integer ID")

            dateformat_resource = references.DateFormat()
            date_format = dateformat_resource.get(value['date_format'])['format']
            value['date_format'] = date_format

        for i, r in enumerate(value['table']):
            if not type(r) is dict:
                raise ValidationError("Table Dict is malformed")

            if not all(k in r for k in required_fields):
                raise ValidationError("Table Dict is malformed, some keys are missing")

            # The date format has to be correct
            format = '%Y-%m-%d'
            if date_format:
                format = date_format

            try:
                datetime.datetime.strptime(r['from'], format)
            except ValueError:
                raise ValidationError("Wrong Date Format in From-Value in Row " + str(i+1))

            try:
                datetime.datetime.strptime(r['to'], format)
            except ValueError:
                raise ValidationError("Wrong Date Format in To-Value Row " + str(i+1))

            # The value has to be a float
            try:
                float(r['value'])
            except ValueError:
                raise ValidationError("At least one value is not a float")

        return value

