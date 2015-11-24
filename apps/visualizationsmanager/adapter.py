"""
Collection of adapters to the Visualisation
"""
from apps.common.serviceadapters.base_adapter import BaseAdapter
from django.conf import settings

__author__ = 'mmilparat'


class DatasetsAdapter(BaseAdapter):
    """
    Adapter for datasets
    """

    def __init__(self):
        dataset_url = settings.PC_SERVICES['references']['base_url'] + \
            settings.PC_SERVICES['references']['datasetsInvisualizations']
        self.url = dataset_url
        self.url_entity = dataset_url + '/%s'
        super(DatasetsAdapter, self).__init__()


class HistoricalEventsAdapter(BaseAdapter):
    """
    Adapter for historical events
    """

    def __init__(self):
        historical_events_url = settings.PC_SERVICES['references']['base_url'] + \
            settings.PC_SERVICES['references']['eventsInVisualizations']
        self.url = historical_events_url
        self.url_entity = historical_events_url + '/%s'
        super(HistoricalEventsAdapter, self).__init__()
