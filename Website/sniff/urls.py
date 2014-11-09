from django.conf.urls import patterns, url

from sniff import views

urlpatterns = patterns('',
    url(r'^find_mac/$', views.find_mac, name='find_mac'),
	url(r'^test/$', views.test, name='test'),
	url(r'^top_devices/$', views.top_devices, name='top_devices'),
	url(r'^enter_shifts/$', views.enter_shifts, name='enter_shifts'),
    url(r'^about/$', views.about, name='about'),
    url(r'^device/(?P<device_mac>[\w\-]+)/$', views.device_locations, name='device_locations'),
	#url(r'^device/([0-9A-F]{2}[:-]){5}([0-9A-F]{2})/$', views.device_locations, name='device_locations'),
	url(r'^device/img/(?P<device_mac>[\w\-]+)/$', views.plot_device_times, name='plot_device_times'),
	url(r'^simple.png', views.simple, name='simple_chart'),
	url(r'^all_devices.png', views.graph_all, name='graph_all'),
	url(r'^analyse_shifts/$', views.analyse_shifts, name='analyse_shifts'),
	url(r'^', views.index, name='index'),
)