__author__ = 'fki'

from rest_framework.serializers import  WritableField, SlugRelatedField
from collections import OrderedDict
from django.core.exceptions import ValidationError
from .models import Dataset
import json
from .dataset_data import DatasetData, TimeResolutions, DatasetDataTransformer

import logging
log = logging.getLogger(__name__)

class DataField(WritableField):

    def field_to_native(self, obj, field):
        params = self.context['request'].QUERY_PARAMS
        dataset_data = DatasetData.from_json(obj.data)

        if 'time_resolution' in params and params['time_resolution']:
            dataset_data.transform_time(params['time_resolution'])

        if 'individuals' in params and params['individuals']:
            individuals = params['individuals']
            individuals = individuals.split(',')
            dataset_data.filter_by_individuals(individuals)

        time_start = None
        time_end = None
        if 'time_start' in params and params['time_start']:
            time_start = params['time_start']

        if 'time_end' in params and params['time_end']:
            time_end = params['time_end']

        if time_start or time_end:
            dataset_data.filter_by_time(time_start, time_end)

        d = DatasetDataTransformer.to_api(dataset_data)
        return d

    def field_from_native(self, data, files, field_name, into):
        if 'data' not in data:
            raise ValidationError("Field 'data' is required.")

        if 'class_id' not in data:
            raise ValidationError('Field class_id is missing.')

        data = DatasetDataTransformer.from_api(
            data[field_name],
            into['time_start'],
            into['time_end'],
            into['time_resolution'],
            data['class_id'],
            data['unit_id']
        )

        result = {
            'data': data.get_json()
        }

        into.update(result)

class TimeField(WritableField):

    def field_to_native(self, obj, field):
        """
        :type obj: Dataset
        :type field: str
        :rtype: str
        :param obj:
        :param field:
        :return:
        """
        try:
            time_dict = OrderedDict([
                ('resolution', obj.time_resolution),
                ('start', obj.time_start),
                ('end', obj.time_end)
            ])
        except AttributeError:
            return None

        return time_dict

    def field_from_native(self, data, files, field_name, into):
        try:
            result = {
                'time_resolution': data['time']['resolution'],
                'time_start': data['time']['start'],
                'time_end': data['time']['end']
            }
        except KeyError as e:
            raise ValidationError('Field ' + str(e) + ' is missing.')
        into.update(result)


class ResourceField(WritableField):

    def field_to_native(self, obj, field):
        """
        :type obj: Dataset
        :type field: str
        :rtype: str
        :param obj:
        :param field:
        :return:
        """
        try:
            if obj.resource_id is not None:
                resource_dict = OrderedDict([
                    ('url', obj.resource_url),
                    ('issued', obj.resource_issued),
                    ('external_resource', obj.resource_id)
                ])
            else:
                resource_dict = OrderedDict([
                    ('url', obj.resource_url),
                    ('issued', obj.resource_issued),
                    ('custom', obj.resource_publisher)
                ])
        except AttributeError:
            return None

        return resource_dict

    def field_from_native(self, data, files, field_name, into):

        if 'resource' in data:
            try:
                result = {
                    'resource_url': data['resource']['url'],
                    'resource_issued': data['resource']['issued'],
                }
            except KeyError as e:
                raise ValidationError('Field ' + str(e) + ' is missing')
            resource = data['resource']
            if 'external_resource' not in resource and 'custom' not in resource:
                raise ValidationError('Either provide external_resource or custom field.')
            else:
                if 'external_resource' in resource:
                    result['resource_id'] = resource['external_resource']
                if 'custom' in resource:
                    result['resource_publisher'] = resource['custom']

            into.update(result)
        else:
            if self.required is False:
                return
            else:
                raise ValidationError('Field resource is missing')


class PolicyDomainSlugRelatedField(SlugRelatedField):

    def to_internal_value(self, data):
        i = 5
        pass
