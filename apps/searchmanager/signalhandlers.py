"""
Signal handlers that should be use from the other apps update the search index.
"""
from django.conf import settings
import threading
import time
import requests
import logging

logger = logging.getLogger(__name__)


class IndexDocumentThread(threading.Thread):
    """
    The indexing process is wrapped in a thread. This is because within the post_save signal the save transaction is not yet committed.
    Therefore when you would call the search index API the database would be locked and the specific item would not yet exist in database
    By using a thread, django commits the transaction and the signal gets asynchronous. Therefore the database is updated when Search Index API is called
    Another solution would be the django-transaction-hooks, but it is experimental and requires a custom database backend to be used.
    """

    def __init__(self, itemid, itemtype, **kwargs):
        self.itemid = itemid
        self.itemtype = itemtype
        super(IndexDocumentThread, self).__init__(**kwargs)

    def run(self):
        # Set sleep time to allow database unlocking and the commit of the save transaction
        time.sleep(5)
        # set the Search - Update Index Item API url for the current item.
        api_url = settings.PC_SERVICES['references']['base_url'] + \
            settings.PC_SERVICES['references']['updateindexitem'] + '/metric/' + str(self.itemid)
        # Execute the API call
        response = requests.post(api_url)

        if response.status_code < 200 or response.status_code >= 300:
            logger.error("Failed while updating search index for {} {}".format(self.itemtype, self.itemid))
        else:
            logger.info("Successfully updated search index for {} {}".format(self.itemtype, self.itemid))
