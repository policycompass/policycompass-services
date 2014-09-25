#
# This is the library with all the required indexing utilities for the Elastic Search
#
from rest_framework.response import Response
from django.conf import settings
import datetime
import urllib
import json,requests

def rebuild_index():
    """
    Rebuilds the index of the Elastic search for the following entities:
    Metrics, Events, Visualizations, FCM models
    TODO: Events, Visualizations, FCM models
    """
    #Load the Metrics objects and index them on Elastic Search server
    #Start logging the indexing process
    indexing_log = 'Indexing service started at '  + str(datetime.datetime.now()) + '.\n'
    #...set the API url for the metrics
    metrics_api_url = settings.PC_SERVICES['references']['base_url'] + '/api/v1/metricsmanager/metrics'
    # Set a counter in order to iterate all the pages
    page = '?page=1'
    while page != 'None' :
       #...Make the api call to get the metrics at current page
       response = urllib.request.urlopen(metrics_api_url + page)
       #...Read the metrics json object returned by the api call
       rawdataresponse = response.read()
       #...Decode the response from bytes to str
       decodeddataresponse = rawdataresponse.decode()
       #...Convert from JSON to python dict
       data = json.loads(decodeddataresponse)
       #Index each item (TODO: use _bulk)
       for item_to_index in data["results"]:
         indexing_log = indexing_log + index_item('metric',item_to_index) + '\n'
       page = str(data["next"])
    return indexing_log

def index_item(itemtype,document):
    #Call the Elastic API Index service (PUT command) to index current document 
    response = requests.put(settings.ELASTICSEARCH_URL+ '/' + itemtype +'/' + str(document["id"]), data=json.dumps(document))
    return response.text
