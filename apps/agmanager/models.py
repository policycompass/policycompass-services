from django.db import models
import logging

log = logging.getLogger(__name__)


class ArgumentationGraph(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    data = models.TextField()

    # Auto-Generated Metadata
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    creator_path = models.CharField(max_length=1024)

    is_draft = models.BooleanField(blank=False, default=False)

    def save(self, *args, **kwargs):
        """
        Saving the data to the database
        """

        super(ArgumentationGraph, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
