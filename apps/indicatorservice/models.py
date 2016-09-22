from django.db import models
import logging

log = logging.getLogger(__name__)


class Indicator(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    # Auto-Generated Metadata
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    creator_path = models.CharField(max_length=1024)

    def __str__(self):
        return self.name
