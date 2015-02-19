from django.conf.urls import patterns, url, include
from .api import UserAuth


user_urls = patterns(
    '',
    url(r'^/signin', UserAuth.as_view()),
)

urlpatterns = patterns(
    '',
    url(r'^users', include(user_urls)),
)