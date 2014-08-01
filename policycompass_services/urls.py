from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
from .api import Base


admin.autodiscover()

urlpatterns = patterns('',

    url(r'^api/v1/eventsmanager/', include('apps.eventsmanager.urls')),
	url(r'^api/v1/metricsmanager/', include('apps.metricsmanager.urls')),
    #url(r'^api/v1/visualizationsmanager/', include('apps.visualizationsmanager.urls')),
    url(r'^api/v1/auth/', include('apps.common.urls')),
    url(r'^api/v1/references/', include('apps.referencepool.urls')),
    url(r'^api/v1/$', Base.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls'), name='swagger'),

    # For the time being redirect to swagger
    url(r'^$', lambda x: HttpResponseRedirect('/app/'))

)
