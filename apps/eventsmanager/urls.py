from django.conf.urls import patterns, url, include
from rest_framework import routers
from .views import HistoricalEventViewSet

router = routers.DefaultRouter()
router.register(r'events', HistoricalEventViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
     url(r'^', include(router.urls)),
)