from django.db import models
from django.core.validators import RegexValidator

class Metric(models.Model):

    # automatically set data
    date_created = models.DateTimeField(auto_now_add=True)
    creator_path = models.CharField(max_length=1024, validators=[ RegexValidator("^(/[^/]*)+/?$") ])

    # metadata stored for humans
    title = models.CharField(max_length=100, unique=True)
    acronym = models.CharField(max_length=20, unique=True)
    description = models.TextField(default="", blank=True)
    keywords = models.CharField(default="", blank=True, max_length=400, validators=[ RegexValidator("^([_\-a-zA-Z0-9]+ ?($|,))+") ])

    indicator_id = models.IntegerField()
    formula = models.TextField()
    variables = models.TextField()
