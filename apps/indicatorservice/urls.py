from django.conf.urls import patterns, url, include
from .api import *
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'indicators', IndicatorViewSet, base_name='indicator')

urlpatterns = patterns(
    '',
    url(r'^$', Base.as_view(), name="indicator-base"),
    url(r'', include(router.urls))
)
