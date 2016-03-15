"""
This creates Django signals that automatically update the elastic search Index
When an item is created, a signal is thrown that runs the create / update index API of the Search Manager
When an item is deleted, a signal is thrown that executes the delete index API of the Search Manager
This way the Policy compass database and Elastic search index remains synced.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Dataset
from apps.searchmanager.signalhandlers import IndexDocumentThread
import requests
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Dataset)
def update_document_on_search_service(sender, **kwargs):
    # Start a new thread for indexing the individual document
    if not kwargs.get('raw', False):
        instance = kwargs['instance']
        IndexDocumentThread(instance.id, 'dataset').start()


@receiver(post_delete, sender=Dataset)
def delete_document_on_search_service(sender, **kwargs):
    # Get current Event details
    curDataset = kwargs['instance']
    # set the Search - Delete Index Item API url for the current event.
    api_url = settings.PC_SERVICES['references']['base_url'] + \
        settings.PC_SERVICES['references']['deleteindexitem'] + '/dataset/' + str(curDataset.id)
    # Execute the API call
    response = requests.post(api_url)
    # Print the response of the API call to console
    if response.status_code < 200 or response.status_code >= 300:
        logger.error("Failed while deleting dataset {} from search index".format(curDataset.id))
    else:
        logger.info("Successfully delted dataset {} from search index".format(curDataset.id))
