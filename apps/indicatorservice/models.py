from django.db import models
import apps.referencepool.models as reference_models
from django.core.exceptions import ValidationError

import logging

log = logging.getLogger(__name__)


class Indicator(models.Model):

    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    units = models.ManyToManyField(reference_models.Unit)
    data_classes = models.ManyToManyField(reference_models.DataClass)
    indicators = models.ManyToManyField('self', blank=True, null=True)
    policy_domain = models.ForeignKey(reference_models.PolicyDomain, blank=True, null=True)

    # ToDo Check that either domain or indicators is set
    # def clean(self):
    #     indic_len = self.indicators.count()
    #     if self.policy_domain is None and indic_len == 0:
    #         raise ValidationError('Please provide a Policy Domain')


    def __str__(self):
        return self.title
