"""
Collection of adapters to the Reference Pool
"""
from .base_adapter import BaseAdapter
from django.conf import settings

__author__ = 'fki'


class Unit(BaseAdapter):
    """
    Adapter for units.
    """

    def __init__(self):
        unit_url = settings.PC_SERVICES['references']['base_url'] + \
            settings.PC_SERVICES['references']['units']
        self.url = unit_url
        self.url_entity = unit_url + '/%s'
        super(Unit, self).__init__()


class Language(BaseAdapter):
    """
    Adapter for languages
    """

    def __init__(self):
        language_url = settings.PC_SERVICES['references']['base_url'] + \
            settings.PC_SERVICES['references']['languages']
        self.url = language_url
        self.url_entity = language_url + '/%s'
        super(Language, self).__init__()


class PolicyDomain(BaseAdapter):
    """
    Adapter for policy domains
    """

    def __init__(self):
        domain_url = settings.PC_SERVICES['references']['base_url'] + \
            settings.PC_SERVICES['references']['domains']
        self.url = domain_url
        self.url_entity = domain_url + '/%s'
        super(PolicyDomain, self).__init__()


class ExternalResource(BaseAdapter):
    """
    Adapter for external resources
    """

    def __init__(self):
        external_resource_url = settings.PC_SERVICES['references']['base_url'] + \
            settings.PC_SERVICES['references']['external_resources']
        self.url = external_resource_url
        self.url_entity = external_resource_url + '/%s'
        super(ExternalResource, self).__init__()


class DateFormat(BaseAdapter):
    """
    Adapter for date format
    """

    def __init__(self):
        dateformat_url = settings.PC_SERVICES['references']['base_url'] + \
            settings.PC_SERVICES['references']['dateformats']
        self.url = dateformat_url
        self.url_entity = dateformat_url + '/%s'
        super(DateFormat, self).__init__()
