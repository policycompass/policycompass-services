"""
Defines all routes of the Dataset Manager
"""

from django.conf.urls import patterns, url, include

from .api import *

urlpatterns = patterns(
    '',
    url(r'^', Base.as_view(), name="dataset-manager-base")
)