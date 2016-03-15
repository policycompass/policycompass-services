"""
This creates Django signals that automatically update the elastic search Index
When an item is created, a signal is thrown that runs the create / update index API of the Search Manager
When an item is deleted, a signal is thrown that executes the delete index API of the Search Manager
This way the Policy compass database and Elastic search index remains synced.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Metric
from apps.searchmanager.signalhandlers import IndexDocumentThread
import requests
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Metric)
def update_document_on_search_service(sender, **kwargs):
    # Start a new thread for indexing the individual document
    if not kwargs.get('raw', False):
        instance = kwargs['instance']
        IndexDocumentThread(instance.id, 'metric').start()


@receiver(post_delete, sender=Metric)
def delete_document_on_search_service(sender, **kwargs):
    # Get current Metric details
    curMetric = kwargs['instance']
    # set the Search - Delete Index Item API url for the current metric.
    api_url = settings.PC_SERVICES['references']['base_url'] + \
        settings.PC_SERVICES['references']['deleteindexitem'] + '/metric/' + str(curMetric.id)
    # Execute the API call
    response = requests.post(api_url)

    if response.status_code < 200 or response.status_code >= 300:
        logger.error("Failed while deleting metric {} from search index".format(curMetric.id))
    else:
        logger.info("Successfully delted metric {} from search index".format(curMetric.id))
