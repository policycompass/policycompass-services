from django.db import models

import logging

log = logging.getLogger(__name__)


class Indicator(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    language = models.IntegerField()
    unit_category = models.IntegerField()

    def __str__(self):
        return self.name


class IndicatorInDomain(models.Model):
    """
    Represents the 1:m relation between an Indicator and Policy Domains
    """
    domain = models.IntegerField()
    # Set the relation
    indicator = models.ForeignKey(Indicator, related_name='policy_domains')

    class Meta:
        verbose_name = "Indicator in Domain"
        verbose_name_plural = "Indicators in Domains"

    def __str__(self):
        return str(self.domain)