"""
Collection of adapters to the Reference Pool
"""

__author__ = 'fki'
from .base_adapter import BaseAdapter
from django.conf import settings


class Unit(BaseAdapter):
    """
    Adapter for units.
    """
    def __init__(self):
        unit_url = settings.PC_SERVICES['references']['base_url'] + settings.PC_SERVICES['references']['units']
        self.url = unit_url
        self.url_entity = unit_url + '/%s'
        super(Unit, self).__init__()


class Language(BaseAdapter):
    """
    Adapter for languages
    """
    def __init__(self):
        language_url = settings.PC_SERVICES['references']['base_url'] + settings.PC_SERVICES['references']['languages']
        self.url = language_url
        self.url_entity = language_url + '/%s'
        super(Language, self).__init__()


class PolicyDomain(BaseAdapter):
    """
    Adapter for policy domains
    """
    def __init__(self):
        domain_url = settings.PC_SERVICES['references']['base_url'] + settings.PC_SERVICES['references']['domains']
        self.url = domain_url
        self.url_entity = domain_url + '/%s'
        super(PolicyDomain, self).__init__()


class ExternalResource(BaseAdapter):
    """
    Adapter for external resources
    """
    def __init__(self):
        external_resource_url = settings.PC_SERVICES['references']['base_url'] + settings.PC_SERVICES['references']['external_resources']
        self.url = external_resource_url
        self.url_entity = external_resource_url + '/%s'
        super(ExternalResource, self).__init__()


class HistoricalEvents(BaseAdapter):
    """
    Adapter for historical events
    """
    def __init__(self):
        historical_events_url = settings.PC_SERVICES['references']['base_url'] + settings.PC_SERVICES['references']['events']
        self.url = historical_events_url
        self.url_entity = historical_events_url + '/%s'
        super(HistoricalEvents, self).__init__()


class Metrics(BaseAdapter):
    """
    Adapter for metrics
    """
    def __init__(self):
        metric_url = settings.PC_SERVICES['references']['base_url'] + settings.PC_SERVICES['references']['metrics']        
        #logging.warning(metric_url)
        self.url = metric_url
        self.url_entity = metric_url + '/%s'
        super(Metrics, self).__init__()
