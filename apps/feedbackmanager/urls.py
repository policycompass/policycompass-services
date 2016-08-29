from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns(
    '',
    url(r'^feedbacks', FeedbackListView.as_view(), name='feedback-list'),
    url(r'^categories', FeedbackCategoryListView.as_view(), name='feedbackcategory-list'),
    url(r'^$', Base.as_view(), name="feedbackmanager-base"),
)
