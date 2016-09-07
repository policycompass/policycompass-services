"""
Defines all routes of the Story Manager
"""

from django.conf.urls import patterns, url
from .api import *

urlpatterns = patterns(
    '',
    url(r'^stories$', StoryView.as_view(), name='story-view'),
    url(r'^stories/(?P<pk>[\d]+)$', StoryDetail.as_view(), name='story-detail'),
    url(r'^chapters$', ChapterView.as_view(), name='chapter-view'),
    url(r'^chapters/(?P<pk>[\d]+)$', ChapterDetail.as_view(), name='chapter-detail'),
    url(r'^contents$', ContentView.as_view(), name='content-view'),
    url(r'^contents/(?P<pk>[\d]+)$', ContentDetail.as_view(), name='content-detail'),
    url(r'^', Base.as_view(), name='storymanager-base')
)
