__author__ = 'fki'

from django.db import models

import logging
log = logging.getLogger(__name__)


class Dataset(models.Model):

    # Basic Metadata Fields
    title = models.CharField(max_length=100, unique=True)
    acronym = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    keywords = models.CharField(max_length=400)
    license = models.CharField(max_length=100, blank=True)

    # Resource Sub-Fields
    resource_url = models.URLField(max_length=500, blank=True)
    resource_issued = models.DateField(blank=True)


    # Foreign API IDs
    spatial = models.IntegerField(blank=True)
    unit = models.IntegerField()
    language = models.IntegerField()
    reference_class = models.IntegerField()  # Actually 'class', but reserved word
    indicator = models.IntegerField()
    # ToDo dimensions
    # ToDo policy_domains

    # Auto-Generated Metadata
    created_at = models.DateTimeField(auto_now_add=True)  # dateAddedtoPC
    updated_at = models.DateTimeField(auto_now=True)  # dateModified
    version = models.IntegerField(editable=False)
    is_applied = models.BooleanField(blank=True, default=False)
    # ToDo applied_details

    # Management Data
    unit_id = models.IntegerField()

    class Meta:
        # Standard sorting by date
        ordering = ['-created_at']

    def __str__(self):
        return self.title
