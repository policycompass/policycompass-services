from django.db import models

class Metric(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    creator = models.IntegerField()

    title = models.CharField(max_length=100, unique=True)
    indicator = models.IntegerField()
    formula = models.TextField()
    variables = models.TextField()
