__author__ = 'fki'

from rest_framework.serializers import ModelSerializer, SortedDictWithMetadata, WritableField
from .models import *
from rest_framework.reverse import reverse
from .fields import *


class DatasetSerializer(ModelSerializer):

    time = TimeField()
    resource = ResourceField(required=False)

    def to_native(self, obj):
        """
        Deserializes the Django model object
        """
        if obj is None:
            return super(DatasetSerializer, self).to_native(obj)

        dataset = super(DatasetSerializer, self).to_native(obj)
        result = SortedDictWithMetadata()
        # Set the self attribute.
        result['self'] = reverse('dataset-detail', args=[obj.pk])
        result.update(dataset)
        return result

    def validate(self, attrs):
        return attrs

    def restore_object(self, attrs, instance=None):
        return super(DatasetSerializer, self).restore_object(attrs, instance)

    class Meta:
        exclude = (
            'time_resolution',
            'time_start',
            'time_end',
            'resource_url',
            'resource_id',
            'resource_issued',
            'resource_publisher'
        )
        fields = ()
        model = Dataset



