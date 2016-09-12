from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
from .api import Base, ExampleAuthenticated, ExampleAdmin
from django.conf import settings
from apps.feedbackmanager.admin import feedback_admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^api/v1/searchmanager/', include('apps.searchmanager.urls')),
    url(r'^api/v1/eventsmanager/', include('apps.eventsmanager.urls')),
    url(r'^api/v1/metricsmanager/', include('apps.metricsmanager.urls')),
    url(r'^api/v1/datasetmanager/', include('apps.datasetmanager.urls')),
    url(r'^api/v1/visualizationsmanager/', include('apps.visualizationsmanager.urls')),
    url(r'^api/v1/ratingsmanager/', include('apps.ratingsmanager.urls')),
    url(r'^api/v1/indicatorservice/', include('apps.indicatorservice.urls')),
    url(r'^api/v1/references/', include('apps.referencepool.urls')),
    url(r'^api/v1/feedbackmanager/', include('apps.feedbackmanager.urls')),
    url(r'^api/v1/storymanager/', include('apps.storymanager.urls')),
    url(r'^api/v1/agmanager/', include('apps.agmanager.urls')),
    url(r'^api/v1/$', Base.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^feedbackadmin/', include(feedback_admin.urls)),
    url(r'^feedback/', lambda x: HttpResponseRedirect('/feedbackadmin/feedbackmanager/feedback')),
    url(r'^docs/', include('rest_framework_swagger.urls'), name='swagger'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.PC_SERVICES['references']['MEDIA_URL'], }),
    url(r'^example/auth/anyuser$', ExampleAuthenticated.as_view()),
    url(r'^example/auth/adminuser$', ExampleAdmin.as_view()),
    # For the time being redirect to swagger
    url(r'^$', lambda x: HttpResponseRedirect('/api/v1'))
)
