__author__ = 'fki'

from rest_framework import serializers
from django.conf import settings
from .serviceadapters import references, base_adapter
import requests

import logging
log = logging.getLogger(__name__)


class ReferenceField(serializers.IntegerField):

    adapter = base_adapter.BaseAdapter

    def field_to_native(self, obj, field_name):
        a = self.adapter()
        id = str(getattr(obj, self.source))
        return a.get(id)


class UnitField(ReferenceField):
    adapter = references.Unit


class LanguageField(ReferenceField):
    adapter = references.Language


class ExternalResourceField(ReferenceField):
    adapter = references.ExternalResource

    def field_to_native(self, obj, field_name):
        id = getattr(obj, self.source)

        if id == 0:
            return None
        else:
            return super(ExternalResourceField, self).field_to_native(obj, field_name)

