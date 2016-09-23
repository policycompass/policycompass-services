from jsonfield import JSONField

from django.db import models
from django.core.validators import RegexValidator


class Metric(models.Model):
    # automatically set data
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    creator_path = models.CharField(max_length=1024, validators=[
        RegexValidator("^(/[^/]*)+/?$")])

    # metadata stored for humans
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(default="", blank=True)
    keywords = models.CharField(default="", blank=True, max_length=400,
                                validators=[RegexValidator(
                                    "^([_\-a-zA-Z0-9]+ ?($|,))+")])

    derived_from_id = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.SET_NULL,
    )
    indicator_id = models.IntegerField()
    formula = models.TextField()
    variables = JSONField()

    is_draft = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return self.title
