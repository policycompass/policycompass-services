from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
from .api import Base
#from config import settings
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/v1/searchmanager/', include('apps.searchmanager.urls')),
    url(r'^api/v1/eventsmanager/', include('apps.eventsmanager.urls')),
	url(r'^api/v1/metricsmanager/', include('apps.metricsmanager.urls')),
    url(r'^api/v1/datasetmanager/', include('apps.datasetmanager.urls')),
    url(r'^api/v1/visualizationsmanager/', include('apps.visualizationsmanager.urls')),
    url(r'^api/v1/indicatorservice/', include('apps.indicatorservice.urls')),
    url(r'^api/v1/auth/', include('apps.common.urls')),
    url(r'^api/v1/references/', include('apps.referencepool.urls')),
    url(r'^api/v1/$', Base.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls'), name='swagger'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.PC_SERVICES['references']['MEDIA_URL'],}),
    # For the time being redirect to swagger
    url(r'^$', lambda x: HttpResponseRedirect('/api/v1'))

)
