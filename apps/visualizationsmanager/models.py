from django.db import models

import datetime
import logging
#from .managers import VisualizationManager, RawDataManager
from .managers import VisualizationManager
#from .utils import get_rawdata_for_visualization, save_rawdata_for_visualization

from apps.metricsmanager.models import Metric

log = logging.getLogger(__name__)


    
class VisualizationType(models.Model):
    type = models.CharField(max_length=100)
    
    
class Visualization(models.Model):

    objects = VisualizationManager()
    # Meta Data by User Input
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    keywords = models.CharField(max_length=200, blank=True)
    #issued = models.DateTimeField()
    publisher = models.CharField(max_length=200, blank=True)
    user_id = models.IntegerField()
    language_id = models.IntegerField()
    # Auto-Generated Meta Data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #version = models.IntegerField(editable=False)
    views_count = models.IntegerField()    
    visualization_type_id = models.IntegerField()
    status_flag_id = models.IntegerField()
    filter_configuration = models.CharField(max_length=200)

   # _rawdata = None

  #  @property
  #  def rawdata(self):
  #      return get_rawdata_for_visualization(self)


  #  @rawdata.setter
  #  def rawdata(self, value):
  #      self._rawdata = value


   # @rawdata.deleter
   # def rawdata(self):
   #     pass
    
    _historical_events_in_visualization = None

    @property
    def historical_events_in_visualization(self):
        return self.historical_events.all()
        

    @historical_events_in_visualization.setter
    def historical_events_in_visualization(self, value):
        self._historical_events_in_visualization = value


    _metrics_in_visualization = None
    @property
    def metrics_in_visualization(self):
        return self.metrics.all()


    @metrics_in_visualization.setter
    def metrics_in_visualization(self, value):
        self._metrics_in_visualization = value

    #def save(self, *args, **kwargs):
    def save(self, *args, **kwargs):
        #logging.warning('save visualization') # will print a message to the console
        
        
        # Increasing the version on every update
        #if self.pk is None:
        #    self.version = 1
        #else:
        #    self.version += 1

        update = False
        
        if self.pk is None:
            update = False
        else:
            update = True
        

        
        super(Visualization, self).save(*args, **kwargs)
        
        if update:
            #logging.warning('--update--')
            
            if (self.historical_events.count()>0):
                #logging.warning('--delete--')
                self.historical_events.all().delete()

            if self._historical_events_in_visualization:   
                     
                 for d_he in self._historical_events_in_visualization:
                    if (d_he['historical_event']):
                        vhe = HistoricalEventsInVisualizations()
                        vhe.visualization_id = self.id
                        vhe.historical_event_id = d_he['historical_event']
                        vhe.description = d_he['description']
                        vhe.save()
             
                
            self.metrics.all().delete()
            if self._metrics_in_visualization:                
                 for d_metrics in self._metrics_in_visualization:
                    self.metrics.create(
                        visualization = self.id,
                        metric_id = d_metrics['metric'],
                        visualization_query = d_metrics['visualization_query']
                    )
                    
        else:
            #logging.warning('--insert--')
            if self._historical_events_in_visualization:
                #logging.warning('--Exist hist. events--')
                for d in self._historical_events_in_visualization:

                    vhe = HistoricalEventsInVisualizations()
                    vhe.visualization_id = self.id
                    vhe.historical_event_id = d['historical_event']
                    vhe.description = d['description']
                    vhe.save()
                     
            if self._metrics_in_visualization:
                logging.warning('--Exist Metrics--')
                for d_metrics in self._metrics_in_visualization:
                    
                    vi_me = MetricsInVisualizations()
                    vi_me.visualization_id = self.id
                    vi_me.metric_id = d_metrics['metric']
                    vi_me.visualization_query = d_metrics['visualization_query']
                    vi_me.save()
                        
        #if self._rawdata:
        #    save_rawdata_for_visualization(self, self._rawdata)

            
            
    def __str__(self):
        return self.title







class MetricsInVisualizations(models.Model):
    #visualization_id = models.IntegerField()
    metric_id = models.IntegerField()
    visualization = models.ForeignKey(Visualization, related_name='metrics')    
    #metric = models.ForeignKey(Metric, related_name='visualizations')
    visualization_query= models.CharField(max_length=200)

    class Meta:
        verbose_name = "Metric in Visualization"
        verbose_name_plural = "Metrics in Visualization"

    def __str__(self):
        return str(self.metric_id)
        
class HistoricalEventsInVisualizations(models.Model):
    #visualization = models.IntegerField()
    #historical_event = models.IntegerField()
    #visualization_id = models.IntegerField()
    visualization = models.ForeignKey(Visualization, related_name='historical_events') 
    historical_event_id = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Historical Event in Visualization"
        verbose_name_plural = "Historical Event in Visualization"

    def __str__(self):
        return str(self.historical_event_id)

