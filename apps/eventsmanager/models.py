from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField(blank=True)
    keywords = models.CharField(max_length=1000, blank=True)
    startEventDate = models.DateTimeField(blank=True)
    endEventDate = models.DateTimeField(blank=True)
    detailsURL = models.URLField(max_length=1000, blank=True)
    geoLocation = models.CharField(max_length=1000, blank=True)
    spatial = models.IntegerField(blank=True, null=True)  # RP individuals
    relatedVisualisation = models.CharField(max_length=1000, blank=True)
    languageID = models.IntegerField()
    userID = models.IntegerField()
    externalResourceID = models.IntegerField(blank=True, default=0)
    dateAddedToPC = models.DateTimeField(auto_now_add=True)
    dateIssuedByExternalResource = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now_add=True)
    viewsCount = models.IntegerField(blank=True)

    creator_path = models.CharField(max_length=1024, default='https://adhocracy-prod.policycompass.eu/api/principals/users/0000000/')

    # Private property to handle the policy domains
    _policy_domains = None

    # Private property to handle the spatials
    _spatials = None

    # Get all Spatial IDs
    @property
    def spatials(self):
        return self.event_spatials.all()

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
            if hasattr(Event, 'self.version'):
                self.version += 1
            else :
                self.version = 2
            update = True

        super(Event, self).save(*args, **kwargs)

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
                self.event_spatials.all().delete()
                # Create new relations
                for s in self._spatials:
                    self.event_spatials.create(spatial=s)
        else:
            if self._policy_domains:
                # Create Policy Domain relations
                for d in self._policy_domains:
                    self.domains.create(domain=d)
            if self._spatials:
                # Create Spatial relations
                for s in self._spatials:
                    self.event_spatials.create(spatial=s)

    def __str__(self):
        return self.title


class EventInDomain(models.Model):
    """
    Represents the 1:m relation between an Event and Policy Domains
    """
    domain = models.IntegerField()
    # Set the relation
    event = models.ForeignKey(Event, related_name='domains')

    class Meta:
        verbose_name = "Event in Domain"
        verbose_name_plural = "Event in Domains"

    def __str__(self):
        return str(self.domain)


class EventInSpatial(models.Model):
    """
    Represents the 1:m relation between a Event and Spatials
    """
    spatial = models.IntegerField()
    # Set the relation
    event = models.ForeignKey(Event, related_name='event_spatials')

    class Meta:
        verbose_name = "Event in Spatial"
        verbose_name_plural = "Event in Spatials"

    def __str__(self):
        return str(self.spatial)


class Extractor(models.Model):
    name = models.CharField(max_length=1000)
    active = models.BooleanField(default=True)
    valid = models.BooleanField(default=True)
