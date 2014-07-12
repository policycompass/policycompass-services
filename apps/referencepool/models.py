from django.db import models


class PolicyDomain(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = "Policy Domain"
        verbose_name_plural = "Policy Domains"

    def __str__(self):
        return self.title


class Language(models.Model):
    code = models.CharField(max_length=2, unique=True)
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"

    def __str__(self):
        return self.title


class ExternalResource(models.Model):
    title = models.CharField(max_length=100, unique=True)
    url = models.URLField()
    api_url = models.URLField()

    class Meta:
        verbose_name = "External Resource"
        verbose_name_plural = "External Resources"

    def __str__(self):
        return self.title

class UnitCategory(models.Model):
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Unit Category"
        verbose_name_plural = "Unit Categories"

    def __str__(self):
        return self.title


class Unit(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    unit_category = models.ForeignKey(UnitCategory)

    class Meta:
        verbose_name = "Unit"
        verbose_name_plural = "Units"

    def __str__(self):
        return self.title