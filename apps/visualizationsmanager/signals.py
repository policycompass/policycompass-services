# This creates Django signals that automatically update the elastic search Index (real-time)
# When an item is created, a signal is thrown that runs the create / update index API of the Search Manager
# When an item is deleted, a signal is thrown that executes the delete index API of the Search Manager
# This way the Policy compass database and Elastic search index remains synced.
# First test to create images
  
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Visualization
import requests
import threading
import time
import logging
from Naked.toolshed.shell import execute_js, muterun_js
import subprocess

@receiver(post_save, sender=Visualization)
def update_document_on_search_service(sender, **kwargs):
     #Get current Visualization details
     curVisualization = kwargs['instance']
     # If current object is inserted / updated without loaddata then index document
     if (kwargs.get('created', True) and not kwargs.get('raw', False)):
         #Start a new thread for indexing the individual document
         indexDocumentThread(curVisualization.id, 'visualization').start()

#@receiver(post_save, sender=Visualization)
#def create_visualisation_image_service(sender, **kwargs):
#      #Get current Visualization details
#      curVisualization = kwargs['instance']
#      createVisualisationImage(curVisualization.id).start()     
     
@receiver(post_delete, sender=Visualization)
def delete_document_on_search_service(sender, **kwargs):
     #Get current Visualization details
     curVisualization = kwargs['instance']
     #set the Search - Delete Index Item API url for the current visualization.
     api_url = settings.PC_SERVICES['references']['base_url'] + settings.PC_SERVICES['references']['deleteindexitem'] + '/visualization/' + str(curVisualization.id)
     # Execute the API call
     response = requests.post(api_url)
     #Print the response of the API call to console
     print(response.text)


#The real-time indexing process is wrapped in a thread. This is because within the post_save signal the save transaction is not yet committed.
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
        api_url = settings.PC_SERVICES['references']['base_url'] + settings.PC_SERVICES['references']['updateindexitem'] + '/visualization/' + str(self.itemid)
        #Execute the API call
        response = requests.post(api_url)
        #Print the response of the API call to console
        print(response.text)

#create image of the svg
class createVisualisationImage(threading.Thread):
    def __init__(self, itemid, **kwargs):
        self.itemid = itemid
        super(createVisualisationImage, self).__init__(**kwargs)

    def run(self):

        logging.warning('----------------------------');
        logging.warning('----------------------------');
        logging.warning('----------------------------');
        logging.warning('--------------->'+str(self.itemid))
        logging.warning('----------------------------');
        logging.warning('----------------------------');
        logging.warning('----------------------------');
                
        #urlFrontEnd = settings.PC_SERVICES['references']['frontend_base_url']+'/app/#/visualizations/graph/'+str(self.itemid);
        urlFrontEnd = settings.PC_SERVICES['references']['frontend_base_url']+'/app/#/visualizations/'+str(self.itemid);
        
        #subprocess.call(['ls', '-1'], shell=True);
        
        ##subprocess.call(["node", "/home/miquel/PolicyCompass/policycompass/policycopmass-services-merged/policycompass-services/apps/visualizationsmanager/phantomCapture/main.js"], shell=True);
        
        
        #subprocess.call(["node", "/home/miquel/PolicyCompass/policycompass/policopmass-services-merged/policycompass-services/apps/visualizationsmanager/phantomCapture/main.js http://localhost:9000/app/#/visualizations/graph/95"], shell=True);
        
        
        #logging.warning('----------------------------2 checkCall ='+str(checkCall));


        #logging.warning('--external_resources-----------------------');
        #logging.warning(str(settings.PC_SERVICES['external_resources']['physical_path_phantomCapture']));
        #logging.warning('--urlFrontEnd-----------------------');
        #logging.warning(str(urlFrontEnd));
        
        
        #stringCall = str(settings.PC_SERVICES['external_resources']['physical_path_phantomCapture'])+" "+str(urlFrontEnd)+str(" visualization ")+str(settings.PC_SERVICES['references']['MEDIA_URL'])+str(" ");
        #logging.warning('--stringCall!!!!!!!!!!!!!!!!!!!!!!!!!!!!!');
        #logging.warning(str(stringCall));
        #logging.warning('--stringCall!!!!!!!!!!!!!!!!!!!!!!!!!!!!!');        
        #subprocess.call(["node", stringCall], shell=True);
        
        
        success = execute_js(str(settings.PC_SERVICES['external_resources']['physical_path_phantomCapture'])+' '+str(urlFrontEnd)+ ' visualization '+str(settings.PC_SERVICES['references']['MEDIA_URL'])+' ');
                    
        
        if success:
            # handle success of the JavaScript
            logging.warning('--handle success of the JavaScript-----------------------');
        else:
            # handle failure of the JavaScript
            logging.warning('--handle failure of the JavaScript-----------------------');
        