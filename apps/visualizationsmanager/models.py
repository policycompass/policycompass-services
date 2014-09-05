from django.db import models

import datetime
import logging
from .managers import VisualizationManager, RawDataManager
from .utils import get_rawdata_for_visualization, save_rawdata_for_visualization

log = logging.getLogger(__name__)


class MetricsInVisualizations(models.Model):
    visualization_id = models.IntegerField()
    metric_id = models.IntegerField()    
    visualization_query= models.CharField(max_length=100)

    class Meta:
        verbose_name = "Metric in Visualization"
        verbose_name_plural = "Metrics in Visualization"

    def __str__(self):
        return str(self.metric_id)
        
class HistoricalEventsInVisualizations(models.Model):
    #visualization = models.IntegerField()
    #historical_event = models.IntegerField()
    visualization_id = models.IntegerField()
    historical_event_id = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Historical Event in Visualization"
        verbose_name_plural = "Historical Event in Visualization"

    def __str__(self):
        return str(self.historical_event_id)

    
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

    _rawdata = None

    @property
    def rawdata(self):
        return get_rawdata_for_visualization(self)


    @rawdata.setter
    def rawdata(self, value):
        self._rawdata = value


    @rawdata.deleter
    def rawdata(self):
        pass



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
        return self.metrics_list.all()
        

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
            logging.warning('--update--')
            
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



class RawData(models.Model):

    objects = RawDataManager()

    visualization = models.ForeignKey(Visualization)
    # Saving the row number, not necessary but convenient
    row = models.PositiveIntegerField()
    value = models.FloatField()
    #from_date = models.DateField()
    #to_date = models.DateField()

    class Meta:
        verbose_name = "Raw Data"
        verbose_name_plural = "Raw Data"
        ordering = ['row']


    def __str__(self):
        return str(self.row) + " Raw Data for " + self.visualization.title


class RawDataCategory(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = "Raw Data Category"
        verbose_name_plural = "Raw Data Categories"

    def __str__(self):
        return self.title


class RawDataExtra(models.Model):
    #visualization = models.ForeignKey(Visualization)
    #category = models.ForeignKey(RawDataCategory)0

    class Meta:
        verbose_name = "Raw Data Extra"
        verbose_name_plural = "Raw Data Extras"
        ordering = ['id']

    def __str__(self):
        return str(self.visualization) 


class RawDataExtraData(models.Model):
    raw_data_extra = models.ForeignKey(RawDataExtra)
    # Saving the row number, not necessary but convenient
    row = models.PositiveIntegerField()
    value = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Raw Data Extra Data"
        verbose_name_plural = "Raw Data Extra Data"
        ordering = ['row']

    def __str__(self):
        return str(self.row) + " " + str(self.raw_data_extra)





