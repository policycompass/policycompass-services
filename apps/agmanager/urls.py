from django.conf.urls import patterns, url, include
from .api import *
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'ags', ArgumentationGraphViewSet, base_name='ag')

urlpatterns = patterns('',
                       url(r'^$',
                           Base.as_view(),
                           name="ag-base"),
                       url(r'', include(router.urls)))
