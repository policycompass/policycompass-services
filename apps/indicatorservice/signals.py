# This creates Django signals that automatically update the elastic search Index
# When an item is created, a signal is thrown that runs the create / update index API of the Search Manager
# When an item is deleted, a signal is thrown that executes the delete index API of the Search Manager
# This way the Policy compass database and Elastic search index remains synced.
  
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Indicator
import requests
import threading
import time

@receiver(post_save, sender=Indicator)
def update_document_on_search_service(sender, **kwargs):
     #Get current Metric details
     curIndicator = kwargs['instance']
     # If current object is inserted / updated without loaddata then index document
     if (kwargs.get('created', True) and not kwargs.get('raw', False)):
         #Start a new thread for indexing the individual document
         indexDocumentThread(curIndicator.id, 'indicator').start()


@receiver(post_delete, sender=Indicator)
def delete_document_on_search_service(sender, **kwargs):
     #Get current Metric details
     curIndicator = kwargs['instance']
     #set the Search - Delete Index Item API url for the current indicator.
     api_url = settings.PC_SERVICES['references']['base_url'] + settings.PC_SERVICES['references']['deleteindexitem'] + '/indicator/' + str(curIndicator.id)
     # Execute the API call
     response = requests.post(api_url)
     #Print the response of the API call to console
     print(response.text)


#The indexing process is wrapped in a thread. This is because within the post_save signal the save transaction is not yet committed.
#Therefore when you would call the search index API the database would be locked and the specific item would not yet exist in database
#By using a thread, django commits the transaction and the signal gets asynchronous. Therefore the database is updated when Search Index API is called
#Another solution would be the django-transaction-hooks, but it is experimental and requires a custom database backend to be used.
class indexDocumentThread(threading.Thread):
    def __init__(self, itemid, itemtype, **kwargs):
        self.itemid = itemid
        self.itemtype = itemtype
        super(indexDocumentThread, self).__init__(**kwargs)

    def run(self):
		#Set sleep time to allow database unlocking and the commit of the save transaction
        time.sleep(5)
        #set the Search - Update Index Item API url for the current item.
        api_url = settings.PC_SERVICES['references']['base_url'] + settings.PC_SERVICES['references']['updateindexitem'] + '/indicator/' + str(self.itemid)
        #Execute the API call
        response = requests.post(api_url)
        #Print the response of the API call to console
        print(response.text)
