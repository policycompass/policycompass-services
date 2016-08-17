from django.conf.urls import patterns, url, include
from .api import *
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'policydomains', PolicyDomainViewSet)
router.register(r'units', UnitViewSet, base_name='unit')
router.register(r'unitcategories', UnitCategoryViewSet)
router.register(r'languages', LanguageViewSet)
router.register(r'externalresources', ExternalResourceViewSet)
router.register(r'dateformats', DateFormatViewSet)
router.register(r'classes', DataClassViewSet, base_name='class')
router.register(r'individuals', IndividualViewSet, base_name='individual')
router.register(r'licenses', LicenseViewSet, base_name='license')

urlpatterns = patterns(
    '',
    url(r'^$', ReferencePool.as_view(), name="reference-base"),
    url(r'', include(router.urls))
)
