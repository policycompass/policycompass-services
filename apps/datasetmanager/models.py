__author__ = 'fki'

from django.db import models

import logging
log = logging.getLogger(__name__)


class Dataset(models.Model):

    RESOLUTIONS = (
        ('year', 'Year'),
        ('month', 'Month'),
        ('day', 'Day'),
        ('decade', 'Decade'),
        ('quarter', 'Quarter')
    )

    # Basic Metadata Fields
    title = models.CharField(max_length=100, unique=True)
    acronym = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    # ToDo Use RP and Foreign Key here
    keywords = models.CharField(max_length=400)

    resource_url = models.URLField(max_length=500, blank=True)
    resource_issued = models.DateField(blank=True)
    resource_id = models.IntegerField(blank=True)  # RP external_resource
    resource_publisher = models.CharField(max_length=100, blank=True)

    is_applied = models.BooleanField(blank=True, default=False)
    metric_id = models.IntegerField(blank=True, null=True)  # MM metric

    spatial = models.IntegerField(blank=True, null=True)  # RP individuals
    license = models.CharField(max_length=100, blank=True)

    version = models.IntegerField(editable=False)

    time_resolution = models.CharField(max_length=10, choices=RESOLUTIONS)
    time_start = models.CharField(max_length=20)
    time_end = models.CharField(max_length=20)

    language_id = models.IntegerField()  # RP languages
    user_id = models.IntegerField()  # UM reference
    unit_id = models.IntegerField()  # RP unit
    indicator_id = models.IntegerField()  # IS indicator
    class_id = models.IntegerField()  # RP class

    # Auto-Generated Metadata
    issued = models.DateTimeField(auto_now_add=True)  # dateAddedtoPC
    modified = models.DateTimeField(auto_now=True)  # dateModified

    # ToDo Fields
    # applied_details
    # dimensions
    # data

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

        super(Dataset, self).save(*args, **kwargs)


    class Meta:
        # Standard sorting by date
        ordering = ['-issued']

    def __str__(self):
        return self.title
