from django.conf.urls import patterns, url, include

from .api import *

unit_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', UnitDetail.as_view(), name='unit-detail'),
    url(r'^$', UnitList.as_view(), name='unit-list')
)

unit_category_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', UnitCategoryDetail.as_view(), name='unit-category-detail'),
    url(r'^$', UnitCategoryList.as_view(), name='unit-category-list')
)

language_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', LanguageDetail.as_view(), name='language-detail'),
    url(r'^$', LanguageList.as_view(), name='language-list')
)

external_resource_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', ExternalResourceDetail.as_view(), name='resource-detail'),
    url(r'^$', ExternalResourceList.as_view(), name='resource-list')
)

policy_domain_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', PolicyDomainDetail.as_view(), name='domain-detail'),
    url(r'^$', PolicyDomainList.as_view(), name='domain-list')
)

urlpatterns = patterns(
    '',
    url(r'^units', include(unit_urls)),
    url(r'^unitcategories', include(unit_category_urls)),
    url(r'^languages', include(language_urls)),
    url(r'^policydomains', include(policy_domain_urls)),
    url(r'^externalresources', include(external_resource_urls)),
    url(r'^', Base.as_view(), name="reference-base")
)