"""
Mock User Model
DEPRECATED
"""

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=50)
    token = models.CharField(max_length=100)

    def __unicode__(self):
        return  self.name
