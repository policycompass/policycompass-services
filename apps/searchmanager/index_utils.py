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
    Metrics, Events, Visualizations, FCM Models, Datasets
    """
    indexing_log = rebuild_index_itemtype('metric')
    indexing_log = indexing_log + rebuild_index_itemtype('visualization')
    indexing_log = indexing_log + rebuild_index_itemtype('event')
    indexing_log = indexing_log + rebuild_index_itemtype('dataset')
    indexing_log = indexing_log + rebuild_index_fcm('fuzzymap')
    return indexing_log

def rebuild_index_itemtype(itemtype):
    """
    Rebuilds the index of the Elastic search for a specific itemtype entity:
    """
    #Start logging the indexing process
    indexing_log = 'Indexing service of ' + itemtype + ' started at '  + str(datetime.datetime.now()) + '.\n'
    #Clear item type on Elastic Search Server
    indexing_log = indexing_log + '\n' + 'Deleting existing indexes: ' + requests.delete(settings.ELASTICSEARCH_URL + itemtype).text + '\n'
    #Init elastic search index mappings for the item type
    indexing_log = indexing_log + init_Index_Mappings(itemtype)
    #Begin indexing - Load the itemtype object (metric,visualization,etc) and index them on Elastic Search server
    #...set the API url for the item type (e.g. metrics api url)
    api_url = settings.PC_SERVICES['references']['base_url'] + '/api/v1/' + itemtype + 'smanager/' + itemtype + 's'
    if itemtype == "dataset":
        api_url = settings.PC_SERVICES['references']['base_url'] + '/api/v1/' + itemtype + 'manager/' + itemtype + 's'

    # Set a counter in order to iterate all the pages
    page = '?page=1'
    while page != 'None' :
       #...Make the api call to get the itemtype (e.g. metric) at current page
       response = urllib.request.urlopen(api_url + page)
       #...Read the itemtype json object returned by the api call
       rawdataresponse = response.read()
       #...Decode the response from bytes to str
       decodeddataresponse = rawdataresponse.decode()
       #...Convert from JSON to python dict
       data = json.loads(decodeddataresponse)
       #Index each item (TODO: use _bulk)
       for item_to_index in data["results"]:
         indexing_log = indexing_log + index_item(itemtype,item_to_index) + '\n'
       page = str(data["next"]).replace(api_url,"")
    return indexing_log

def index_item(itemtype,document):
    """
    Indexs a single document to the elastic search
    """
    item_id = str(document["id"])
    #Call the Elastic API Index service (PUT command) to index current document 
    response = requests.put(settings.ELASTICSEARCH_URL + itemtype +'/' + item_id, data=json.dumps(document))
    return response.text

def update_index_item(itemtype,item_id):
    """
    Creates or updates a document index based on its id.To be used by external apps when creating / updating an object
    """
     #Set the API url for the item type (e.g. metrics api url)
    if itemtype == 'fuzzymap': 
        api_url = settings.PC_SERVICES['references']['fcm_base_url'] + '/api/v1/' + 'fcmmanager/models'
    else:
        api_url = settings.PC_SERVICES['references']['base_url'] + '/api/v1/' + itemtype + 'smanager/' + itemtype + 's'
    if itemtype == "dataset":
        api_url = settings.PC_SERVICES['references']['base_url'] + '/api/v1/' + itemtype + 'manager/' + itemtype + 's'
    #Make the api call to get the itemtype (e.g. metric) with the specific id
    response = urllib.request.urlopen(api_url + '/' + str(item_id))
    #Read the itemtype json object returned by the api call
    rawdataresponse = response.read()
    #Decode the response from bytes to str
    decodeddataresponse = rawdataresponse.decode()
    #Convert from JSON to python dict
    data = json.loads(decodeddataresponse)
    #Remove the data container specifically of the metrics object that contains a lot of table information
    data.pop("data", None)
        #Remove the data container specifically of the metrics object that contains a lot of table information
    data.pop("data", None)  
    #Call the Elastic API Index service (PUT command) to index current document 
    if itemtype == 'fuzzymap':
        response = requests.put(settings.ELASTICSEARCH_URL + itemtype +'/' + str(data["model"]["id"]), data=json.dumps(data["model"]))
    else:
        response = requests.put(settings.ELASTICSEARCH_URL + itemtype +'/' + str(data["id"]), data=json.dumps(data))
    return response.text

def delete_index_item(itemtype,item_id):
    """
    Delete the index of a document based on its id.To be used by external apps when deleting the actual object
    """
    #Call the Elastic API Index service (PUT command) to index current document 
    response = requests.delete(settings.ELASTICSEARCH_URL + itemtype +'/' + str(item_id))
    return response.text
  
def init_Index_Mappings(itemtype):
    """
    Init the elastic search mappings of the document of the index
    """
    #Check if index already exists and if it doesn't create it
    if ((requests.head(settings.ELASTICSEARCH_URL).status_code) != 200):
		#Set a case insensite sort analyzer (see http://www.elastic.co/guide/en/elasticsearch/guide/current/sorting-collations.html)
        mysettings = '{"settings": {"analysis": {"analyzer": {"case_insensitive_sort": {"tokenizer": "keyword","filter":  [ "lowercase" ]}}}}}'
        response = requests.put(settings.ELASTICSEARCH_URL,data=mysettings)
    #Prepare the mapping instructions
    mapping = '{"' + itemtype + '": {"properties": {"title": {"type": "string", "fields": {"lower_case_sort": { "type":  "string", "analyzer": "case_insensitive_sort"} }	} }	}}'
    #Call the Elastic API Index service (PUT command) to set the mappings of current document 
    response = requests.put(settings.ELASTICSEARCH_URL + '_mapping/' + itemtype,data = mapping)
    return '\n' + 'Init Index Mappings: ' + response.text + '\n'

def rebuild_index_fcm(itemtype):
    """
    Rebuilds the index of the Elastic search for FCM models.To optimize this code FCM API needs to be consistent with the rest APIs
    """
    #Start logging the indexing process
    indexing_log = 'Indexing service of ' + itemtype + ' started at '  + str(datetime.datetime.now()) + '.\n'
    #Clear item type on Elastic Search Server
    indexing_log = indexing_log + '\n' + 'Deleting existing indexes: ' + requests.delete(settings.ELASTICSEARCH_URL + itemtype).text + '\n'
    #Init elastic search index mappings for the item type
    indexing_log = indexing_log + init_Index_Mappings(itemtype)
    #Begin indexing - Load the itemtype object (metric,visualization,etc) and index them on Elastic Search server
    #...set the API url for the item type (e.g. fuzzy api url) 
    api_url = settings.PC_SERVICES['references']['fcm_base_url'] + '/api/v1/' + 'fcmmanager/models'
    #...Make the api call to get the itemtype (e.g. fuzzy) at current page
    response = urllib.request.urlopen(api_url)
    #...Read the itemtype json object returned by the api call
    rawdataresponse = response.read()
    #...Decode the response from bytes to str
    decodeddataresponse = rawdataresponse.decode()
    #...Convert from JSON to python dict
    data = json.loads(decodeddataresponse)
    #Index each item (TODO: use _bulk)
    for item_to_index in data:
      indexing_log = indexing_log + index_item(itemtype,item_to_index) + '\n'
    return indexing_log
