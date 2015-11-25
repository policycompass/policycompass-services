from django.db import models
import logging

log = logging.getLogger(__name__)


class Indicator(models.Model):
    name = models.CharField(max_length=100, unique=True)
    acronym = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    language = models.IntegerField()
    unit_category = models.IntegerField()

    # Auto-Generated Metadata
    issued = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    creator_path = models.CharField(max_length=1024)

    # Private property to handle the policy domains
    _policy_domains = None

    # Get all Policy Domain IDs
    @property
    def policy_domains(self):
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
        if self.pk:
            update = True

        super(Indicator, self).save(*args, **kwargs)

        # When it is just an update
        if update:
            if self._policy_domains:
                # Delete olf policy domain relations
                self.domains.all().delete()
                # Create new relations
                for d in self._policy_domains:
                    self.domains.create(domain=d)
        else:
            if self._policy_domains:
                # Create Policy Domain relations
                for d in self._policy_domains:
                    self.domains.create(domain=d)

    def __str__(self):
        return self.name


class IndicatorInDomain(models.Model):
    """
    Represents the 1:m relation between an Indicator and Policy Domains
    """
    domain = models.IntegerField()
    # Set the relation
    indicator = models.ForeignKey(Indicator, related_name='domains')

    class Meta:
        verbose_name = "Indicator in Domain"
        verbose_name_plural = "Indicators in Domains"

    def __str__(self):
        return str(self.domain)
