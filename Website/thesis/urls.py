from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'thesis.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('sniff.urls', namespace='sniff', app_name='sniff')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chat/', include('djangoChat.urls')),
)
