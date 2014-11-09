
from django.shortcuts import render,redirect
from django.template import RequestContext, loader
from django.http import HttpResponse
from sniff.models import *
from django.db.models import Count
import time
import os
from forms import *
import random
import django
import datetime
from analyse import *
from plot import *

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

os.environ['TZ'] = 'Australia/Brisbane'
time.tzset()

# Create your views here.


def index(request):
    context = {
    }
    return render(request, 'sniff/index.html', context)

def top_devices(request):
    #highest_macs = FoundDevices.objects.all()[:20]
	base_stations = load_base_stations()
	top_devices = FoundDevices.objects.values('mac_address').exclude(mac_address__in=base_stations).annotate(count=Count('mac_address')).order_by('-count')[:500]
	for device in top_devices:
		device['url_mac'] = device['mac_address'].replace(':','-')
	context = {
		'top_devices': top_devices,
	}
	return render(request, 'sniff/top_devices.html', context)

def find_mac(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = AddressForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
			mac_address = form.cleaned_data['mac_address'].replace(':','-')
			return redirect('/device/%s/' %mac_address)
		else:
			mac_address = form.cleaned_data['mac_address'].replace(':','-')
			return device_locations(request, mac_address)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddressForm()

    return render(request, 'sniff/find_mac.html', {'form': form})

def enter_shifts(request):
	context = {}
	return render(request, 'sniff/enter_shifts.html', context)
	
def test(request):
	base_stations = load_base_stations()
	top_devices = FoundDevices.objects.values('mac_address').exclude(mac_address__in=base_stations).annotate(count=Count('mac_address')).order_by('-count')[:20]
	for device in top_devices:
		device['url_mac'] = device['mac_address'].replace(':','-')
	context = {
		'top_devices': top_devices,
	}
	return render(request, 'sniff/test.html', context)
	
def analyse_shifts(request):
	if request.method == 'POST':
		days = ['mon','tues','wed','thurs','fri','sat']
		context = {}
		context['data'] = request.POST
		
		shifts = {}
		times = []
		for day in days:
			try:
				start = datetime.datetime.strptime(request.POST[day+'_start'], '%d %m %Y - %H:%M')
				shift_days = start.weekday()
				shift = datetime.timedelta(days = shift_days)
				week_start = datetime.datetime(start.year,start.month,start.day) - shift
				
			except:
				start = None
			try:
				end = datetime.datetime.strptime(request.POST[day+'_end'], '%d %m %Y - %H:%M')
			except:
				end = None
				
			if start and end:
				times.append((start,end))
			shifts[day] = (start,end)
		
			
		
		
		
		context['shifts'] = shifts
		context['week_start'] = week_start
		
		base_stations = load_base_stations()
		
	
		found_devices = get_found_devices(base_stations=base_stations)
		context['devices'] = track_shift(times,found_devices,'0',week_start,base_stations,verbose=False)
		return render(request, 'sniff/analyse_shifts.html', context)
	else:
		return redirect('/enter_shifts/')
		
	
	
def device_locations(request, device_mac):
	devices = FoundDevices.objects.all().filter(mac_address=device_mac.replace('-',':'))
	for i in range(len(devices)):
		devices[i].time = time.strftime("%d-%m-%y %H:%M", time.localtime(float(devices[i].time)))
	context = {'devices': devices,'mac_address':device_mac}
	context['device_url'] = '/device/%s/' %device_mac.replace(':','-')
	return render(request, 'sniff/device_locations.html', context)


def about(request):
	context = {}
	return render(request, 'sniff/about.html', context)
	
	
def simple(request):
    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d')) 
    
	#fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
	
def graph_all(request):
	base_stations = load_base_stations()
	found_devices = get_found_devices(base_stations=base_stations)
	#found_devices = import_from_csv()
	
	count = count_minutes(found_devices,base_stations)
	return plot_activity(count)

def plot_device_times(request, device_mac):
	device_mac = device_mac.replace('-',':').lower()
	base_stations = load_base_stations()
	
	#found_devices = get_found_devices(base_stations=base_stations)
	#found_devices = import_from_csv()
	current_device_values = device_values(device_mac,base_stations)
	
	
	return plot_device(current_device_values,device_mac)