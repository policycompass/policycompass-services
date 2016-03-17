"""
This creates Django signals that automatically update the elastic search Index (real-time)
When an item is created, a signal is thrown that runs the create / update index API of the Search Manager
When an item is deleted, a signal is thrown that executes the delete index API of the Search Manager
This way the Policy compass database and Elastic search index remains synced.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Visualization
from apps.searchmanager.signalhandlers import search_index_update, search_index_delete


@receiver(post_save, sender=Visualization)
def update_document_on_search_service(sender, **kwargs):
    if not kwargs.get('raw', False):
        instance = kwargs['instance']
        search_index_update('visualization', instance.id)


@receiver(post_delete, sender=Visualization)
def delete_document_on_search_service(sender, **kwargs):
    instance = kwargs['instance']
    search_index_delete('visualization', instance.id)
