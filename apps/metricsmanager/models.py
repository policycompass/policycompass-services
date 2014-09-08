"""
Defines all models, which are representing database entities,
"""
from django.db import models

import logging
from .utils import get_rawdata_for_metric, save_rawdata_for_metric, update_rawdata_for_metric

log = logging.getLogger(__name__)


class Metric(models.Model):
    """
    The model for the metadata of a metric
    """
    # Meta Data by User Input
    title = models.CharField(max_length=100, unique=True)
    acronym = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    keywords = models.CharField(max_length=400)

    geo_location = models.CharField(max_length=1000, blank=True)

    publisher = models.CharField(max_length=200, blank=True)
    details_url = models.URLField(max_length=500, blank=True)
    publisher_issued = models.DateField(blank=True, null=True)

    license = models.CharField(max_length=100, blank=True)

    unit_id = models.IntegerField()
    user_id = models.IntegerField()
    language_id = models.IntegerField()
    ext_resource_id = models.IntegerField(blank=True,default=0)
    formula = models.CharField(max_length=10000, default='1')

    # Auto-Generated Meta Data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.IntegerField(editable=False)

    # Private property to handle the raw data
    _rawdata = None

    # Get the raw data
    @property
    def rawdata(self):
        # Use the util module to actually get it
        return get_rawdata_for_metric(self)

    # Set the raw data
    @rawdata.setter
    def rawdata(self, value):
        self._rawdata = value

    # Delete the raw data
    @rawdata.deleter
    def rawdata(self):
        # Not implemented yet, works automatically by Django cascading logic
        pass

     # Private property to handle the policy domains
    _policy_domains = None

    # Get all Policy Domain IDs
    @property
    def policy_domains(self):
        # Defined in MetricInDomain
        return self.domains.all()

    # Set the list of policy domains
    @policy_domains.setter
    def policy_domains(self, value):
        self._policy_domains = value

    def save(self, *args, **kwargs):
        """
        Saving the data to the database
        """
        update = False

        # Increasing the version on every update
        if self.pk is None:
            self.version = 1
        else:
            self.version += 1
            update = True

        super(Metric, self).save(*args, **kwargs)

        # When it is just an update
        if update:
            if self._rawdata:
                # Update the raw data
                update_rawdata_for_metric(self, self._rawdata)
            if self._policy_domains:
                # Delete olf policy domain relations
                self.domains.all().delete()
                # Create new relations
                for d in self._policy_domains:
                    self.domains.create(
                        domain_id = d
                    )
        else:
            if self._rawdata:
                # Create the raw data
                save_rawdata_for_metric(self, self._rawdata)
            if self._policy_domains:
                # Create Policy Domain relations
                for d in self._policy_domains:
                    self.domains.create(
                        domain_id = d
                    )

    class Meta:
        # Standard sorting by date
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class MetricInDomain(models.Model):
    """
    Represents the 1:m relation between a Metric and Policy Domains
    """
    domain_id = models.IntegerField()
    # Set the relation
    metric = models.ForeignKey(Metric, related_name='domains')

    class Meta:
        verbose_name = "Metric in Domain"
        verbose_name_plural = "Metrics in Domains"

    def __str__(self):
        return str(self.domain_id)


class RawData(models.Model):
    """
    Represents the basic raw data with times, value and row number
    """
    metric = models.ForeignKey(Metric)
    # Saving the row number, not necessary but convenient
    row = models.PositiveIntegerField()
    value = models.FloatField()
    from_date = models.DateField()
    to_date = models.DateField()

    class Meta:
        verbose_name = "Raw Data"
        verbose_name_plural = "Raw Data"
        # Standard sorting by row
        ordering = ['row']

    def __str__(self):
        return str(self.row) + " Raw Data for " + self.metric.title


class RawDataCategory(models.Model):
    """
    Represents the available extra columns categories
    """
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = "Raw Data Category"
        verbose_name_plural = "Raw Data Categories"

    def __str__(self):
        return self.title


class RawDataExtra(models.Model):
    """
    Links a Metric to its extra columns
    """
    metric = models.ForeignKey(Metric)
    # An extra column has a category
    category = models.ForeignKey(RawDataCategory)

    class Meta:
        verbose_name = "Raw Data Extra"
        verbose_name_plural = "Raw Data Extras"
        ordering = ['id']

    def __str__(self):
        return str(self.metric) + " - " + str(self.category)


class RawDataExtraData(models.Model):
    """
    Represents the actual value of an extra columns
    """
    # Link to the extra column
    raw_data_extra = models.ForeignKey(RawDataExtra)
    row = models.PositiveIntegerField()
    value = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Raw Data Extra Data"
        verbose_name_plural = "Raw Data Extra Data"
        ordering = ['row']

    def __str__(self):
        return str(self.row) + " " + str(self.raw_data_extra)





