from django.db import models
import logging
from django.core.validators import RegexValidator

log = logging.getLogger(__name__)


class VisualizationType(models.Model):
    type = models.CharField(max_length=100)


class Visualization(models.Model):
    # Meta Data by User Input
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    keywords = models.CharField(max_length=200, blank=True)
    # issued = models.DateTimeField()
    # publisher = models.CharField(max_length=200, blank=True)
    # user_id = models.IntegerField()
    language_id = models.IntegerField()
    location = models.IntegerField(blank=True, null=True)

    # Auto-Generated Meta Data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator_path = models.CharField(max_length=1024, validators=[
        RegexValidator("^(/[^/]*)+/?$")])

    views_count = models.IntegerField()
    visualization_type_id = models.IntegerField()
    status_flag_id = models.IntegerField()
    filter_configuration = models.CharField(max_length=800)

    _historical_events_in_visualization = None

    # Private property to handle the policy domains
    _policy_domains = None

    # Get all Policy Domain IDs
    @property
    def policy_domains(self):
        return self.domains.all()

    # Set the list of policy domains
    @policy_domains.setter
    def policy_domains(self, value):
        self._policy_domains = value

    @property
    def historical_events_in_visualization(self):
        return self.historical_events.all()

    @historical_events_in_visualization.setter
    def historical_events_in_visualization(self, value):
        self._historical_events_in_visualization = value

    _datasets_in_visualization = None

    @property
    def datasets_in_visualization(self):
        return self.datasets.all()

    @datasets_in_visualization.setter
    def datasets_in_visualization(self, value):
        self._datasets_in_visualization = value

    def save(self, *args, **kwargs):
        update = False

        if self.pk is None:
            update = False
        else:
            update = True

        super(Visualization, self).save(*args, **kwargs)

        if update:
            if self._policy_domains:
                # Delete olf policy domain relations                                
                self.domains.all().delete()
                # Create new relations
                for d in self._policy_domains:
                    self.domains.create(domain=d)

            if (self.historical_events.count() > 0):
                self.historical_events.all().delete()
            if self._historical_events_in_visualization:
                for d_he in self._historical_events_in_visualization:
                    if (d_he['historical_event']):
                        vhe = HistoricalEventsInVisualizations()
                        vhe.visualization_id = self.id
                        vhe.historical_event_id = d_he['historical_event']
                        vhe.description = d_he['description']
                        vhe.color = d_he['color']
                        vhe.save()

            self.datasets.all().delete()
            if self._datasets_in_visualization:
                for d_datasets in self._datasets_in_visualization:
                    if (d_datasets['dataset']):
                        self.datasets.create(
                            visualization=self.id,
                            dataset_id=d_datasets['dataset'],
                            visualization_query=d_datasets[
                                'visualization_query']
                        )


        else:

            if self._policy_domains:
                # Create Policy Domain relations
                for d in self._policy_domains:
                    self.domains.create(domain=d)

            if self._historical_events_in_visualization:
                for d in self._historical_events_in_visualization:
                    vhe = HistoricalEventsInVisualizations()
                    vhe.visualization_id = self.id
                    vhe.historical_event_id = d['historical_event']
                    vhe.description = d['description']
                    vhe.color = d['color']
                    vhe.save()

            if self._datasets_in_visualization:
                for d_datasets in self._datasets_in_visualization:
                    vi_me = DatasetsInVisualizations()
                    vi_me.visualization_id = self.id
                    vi_me.dataset_id = d_datasets['dataset']
                    vi_me.visualization_query = d_datasets[
                        'visualization_query']
                    vi_me.save()

    def __str__(self):
        return self.title


class DatasetsInVisualizations(models.Model):
    dataset_id = models.IntegerField()
    visualization = models.ForeignKey(Visualization, related_name='datasets')
    visualization_query = models.CharField(max_length=800)

    class Meta:
        verbose_name = "Dataset in Visualization"
        verbose_name_plural = "Datasets in Visualization"

    def __str__(self):
        return str(self.dataset_id)


class HistoricalEventsInVisualizations(models.Model):
    visualization = models.ForeignKey(Visualization,
                                      related_name='historical_events')
    historical_event_id = models.IntegerField()
    description = models.TextField(blank=True)
    color = models.TextField(blank=True, default='')

    class Meta:
        verbose_name = "Historical Event in Visualization"
        verbose_name_plural = "Historical Event in Visualization"

    def __str__(self):
        return str(self.historical_event_id)


class VisualizationInDomain(models.Model):
    """
    Represents the 1:m relation between an Visualization and Policy Domains
    """
    domain = models.IntegerField()
    # Set the relation
    visualization = models.ForeignKey(Visualization, related_name='domains')

    class Meta:
        verbose_name = "Visualization in Domain"
        verbose_name_plural = "Visualization in Domains"

    def __str__(self):
        return str(self.domain)
