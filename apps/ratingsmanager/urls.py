from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns(
    '',
    url(r'^ratings$', RatingsListView.as_view(), name='ratings-list'),
    url(r'^ratings/(?P<identifier>\w+)$', RatingDetailView.as_view(), name='rating-instance'),
    url(r'^$', Base.as_view(), name="ratingsmanager-base"),
)
