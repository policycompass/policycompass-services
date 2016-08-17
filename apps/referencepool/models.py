from django.db import models


class PolicyDomain(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    class Meta:
        ordering = ['title']
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
        ordering = ['title']

    def __str__(self):
        return self.title


class ExternalResource(models.Model):
    title = models.CharField(max_length=100, unique=True)
    url = models.URLField()
    api_url = models.URLField()

    class Meta:
        verbose_name = "External Resource"
        verbose_name_plural = "External Resources"
        ordering = ['title']

    def __str__(self):
        return self.title


class UnitCategory(models.Model):
    title = models.CharField(max_length=100, unique=True)
    identifier = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Unit Category"
        verbose_name_plural = "Unit Categories"
        ordering = ['title']

    def __str__(self):
        return self.title


class Unit(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    unit_category = models.ForeignKey(UnitCategory)
    identifier = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Unit"
        verbose_name_plural = "Units"
        ordering = ['title']

    def __str__(self):
        return self.title


class DateFormat(models.Model):
    """
    Holds different formats for dates
    """
    # Based on https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
    format = models.CharField(max_length=50, unique=True)
    example = models.CharField(max_length=50)
    # Based on http://en.wikipedia.org/wiki/Date_format_by_country
    symbol = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Date Format"
        verbose_name_plural = "Date Formats"

    def __str__(self):
        return self.example


class DataClass(models.Model):
    """
    Refers to a Policy Compass Class
    """
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    code_type = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ['title']

    def __str__(self):
        return self.title


class Individual(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=30, blank=True)
    data_class = models.ForeignKey(DataClass)

    class Meta:
        verbose_name = "Individual"
        verbose_name_plural = "Individuals"
        ordering = ['title']

    def __str__(self):
        return self.title


class License(models.Model):
    title = models.CharField(max_length=200, unique=True)
    identifier = models.CharField(max_length=100, unique=True)
    url = models.URLField()

    class Meta:
        verbose_name = "License"
        verbose_name_plural = "Licenses"
        ordering = ['title']

    def __str__(self):
        return self.title
