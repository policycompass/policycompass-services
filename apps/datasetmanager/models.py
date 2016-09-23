import logging
from django.db import models

__author__ = 'fki'

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
    description = models.TextField()
    # ToDo Use RP and Foreign Key here
    keywords = models.CharField(max_length=400)

    resource_url = models.URLField(max_length=500, blank=True)
    resource_issued = models.DateField(blank=True)
    # RP external_resource
    resource_id = models.IntegerField(blank=True, null=True)
    resource_publisher = models.CharField(max_length=100, blank=True)

    spatial = models.IntegerField(blank=True, null=True)  # RP individuals

    is_applied = models.BooleanField(blank=True, default=False)
    metric_id = models.IntegerField(blank=True, null=True)  # MM metric

    license = models.CharField(max_length=100, blank=True)

    license_id = models.IntegerField(blank=True, null=True)

    version = models.IntegerField(editable=False)

    time_resolution = models.CharField(max_length=10, choices=RESOLUTIONS)
    time_start = models.CharField(max_length=20)
    time_end = models.CharField(max_length=20)

    language_id = models.IntegerField()  # RP languages
    creator_path = models.CharField(max_length=1024)
    unit_id = models.IntegerField()  # RP unit
    indicator_id = models.IntegerField()  # IS indicator
    class_id = models.IntegerField()  # RP class

    # Auto-Generated Metadata
    date_created = models.DateTimeField(auto_now_add=True)  # dateAddedtoPC
    date_modified = models.DateTimeField(auto_now=True)  # dateModified

    data = models.TextField()

    is_draft = models.BooleanField(blank=False, default=False)

    # ToDo Fields
    # applied_details
    # dimensions
    # data

    # Private property to handle the policy domains
    _policy_domains = None

    # Private property to handle the spatials
    _spatials = None

    # Get all Spatial IDs
    @property
    def spatials(self):
        return self.dataset_spatials.all()

    @spatials.setter
    def spatials(self, value):
        self._spatials = value

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
        # Increasing the version on every update
        if self.pk is None:
            self.version = 1
        else:
            self.version += 1
            update = True

        super(Dataset, self).save(*args, **kwargs)

        # When it is just an update
        if update:
            if self._policy_domains:
                # Delete olf policy domain relations
                self.domains.all().delete()
                # Create new relations
                for d in self._policy_domains:
                    self.domains.create(domain=d)
            if self._spatials:
                # Delete olf policy domain relations
                self.dataset_spatials.all().delete()
                # Create new relations
                for s in self._spatials:
                    self.dataset_spatials.create(spatial=s)
        else:
            if self._policy_domains:
                # Create Policy Domain relations
                for d in self._policy_domains:
                    self.domains.create(domain=d)
            if self._spatials:
                # Create Spatial relations
                for s in self._spatials:
                    self.dataset_spatials.create(spatial=s)

    class Meta:
        # Standard sorting by date
        ordering = ['-date_created']

    def __str__(self):
        return self.title


class DatasetInDomain(models.Model):
    """
    Represents the 1:m relation between an Indicator and Policy Domains
    """
    domain = models.IntegerField()
    # Set the relation
    dataset = models.ForeignKey(Dataset, related_name='domains')

    class Meta:
        verbose_name = "Dataset in Domain"
        verbose_name_plural = "Dataset in Domains"

    def __str__(self):
        return str(self.domain)


class DatasetInSpatial(models.Model):
    """
    Represents the 1:m relation between a Dataset and Spatials
    """
    spatial = models.IntegerField()
    # Set the relation
    dataset = models.ForeignKey(Dataset, related_name='dataset_spatials')

    class Meta:
        verbose_name = "Dataset in Spatial"
        verbose_name_plural = "Dataset in Spatials"

    def __str__(self):
        return str(self.spatial)
