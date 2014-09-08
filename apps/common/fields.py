"""
Custom Fields for resolving references to Reference Pool
"""

__author__ = 'fki'

from rest_framework import serializers
from django.conf import settings
from .serviceadapters import references, base_adapter
import requests

import logging
log = logging.getLogger(__name__)


class ReferenceField(serializers.IntegerField):
    """
    Base field for all Reference Pool Fields.
    It uses the service adapters to retrieve the data.
    Specific Implementations must override the adapter property.
    """
    # Initialize the adapter
    adapter = base_adapter.BaseAdapter

    def field_to_native(self, obj, field_name):
        a = self.adapter()
        id = str(getattr(obj, self.source))
        return a.get(id)


class UnitField(ReferenceField):
    """
    Field for a unit
    """
    adapter = references.Unit


class LanguageField(ReferenceField):
    """
    Field for the language
    """
    adapter = references.Language


class ExternalResourceField(ReferenceField):
    """
    Field for an external resource
    """
    adapter = references.ExternalResource


    def field_to_native(self, obj, field_name):
        """
        Customization of the serialization, because the external resource can be None.
        """
        id = getattr(obj, self.source)

        if id == 0:
            return None
        else:
            return super(ExternalResourceField, self).field_to_native(obj, field_name)

