from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pc_datamanager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^api/v1/', include('metricsmanager.urls')),
    #url(r'^api/v1/auth/', include('apps.user_mgmt_mock.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls'), name='swagger'),
    # For the time being redirect to swagger
    url(r'^$', lambda x: HttpResponseRedirect('/app/'))

)
