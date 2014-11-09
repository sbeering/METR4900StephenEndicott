from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from sniff.models import *
from django.db.models import Count
from django.conf import settings

import MySQLdb as mysql
import csv
import os
import time, datetime
import math
from urllib2 import urlopen

import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter,HourLocator,DayLocator
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter



def plot_activity(values):

	daysFmt = DateFormatter("%d-%B %H:00")

	fig=Figure()
	ax=fig.add_subplot(111)

	times = values.keys()
	times.sort()

	number_found = [values[key] for key in times]

	ax.plot_date(times, number_found, '-')
	
	#assert 0, '%s'%(values)

	# format the ticks
	ax.xaxis.set_major_locator(HourLocator(byhour=range(0,24,4)))
	ax.xaxis.set_major_formatter(daysFmt)
	ax.autoscale_view()
	ax.grid(True)
	ax.set_title('All devices')

	fig.autofmt_xdate()
	canvas=FigureCanvas(fig)
	response=HttpResponse(content_type='image/png')
	canvas.print_png(response)
	return response
	


def plot_device(values,mac_address=''):

	daysFmt = DateFormatter("%d-%B %H:00")

	col = ['g','b','c','m','y','r']
	counter = 0

	fig=Figure()
	ax=fig.add_subplot(111)
	#Get all the stations the device went through and plot them
	stations = set()

	times = values.keys()
	times.sort()


	for key in values.keys():
		for station in values[key]['stations'].keys():
			stations.add(station)
	print stations
	#Plot the staions on seperate graphes
	for station in stations:
		print "currently station: ",station
		number_found= []

		for key in times:
			print "currently entry: ",key,' ',values[key]['stations']
			number_found.append(values[key]['stations'][station])



		times = values.keys()
		times.sort()


		
		ax.plot(times, number_found, col[counter]+'-',label=str(station))
		counter += 1

	number_found = []
	for time in times:
		count = 0
		for key in values[time]['stations'].keys():
			count += values[time]['stations'][key]
		number_found.append(count)


	ax.plot(times, number_found, col[counter]+'-',label='total',alpha=.4)

	# format the ticks
	d_time = max(times) - min(times)
	if d_time <= datetime.timedelta(days = 7):
		ax.xaxis.set_major_locator(HourLocator(byhour=range(0,24,2)))
	elif datetime.timedelta(days = 7) < d_time < datetime.timedelta(days = 31):
		ax.xaxis.set_major_locator(HourLocator(byhour=range(0,24,12)))
	elif datetime.timedelta(days = 31) < d_time :
		ax.xaxis.set_major_locator(DayLocator())

	ax.xaxis.set_major_formatter(daysFmt)
	ax.autoscale_view()
	ax.grid(True)

	fig.autofmt_xdate()
	ax.legend(loc='upper right')
	ax.set_title('%s'%mac_address)
	DPI = 144.0
	fig.set_size_inches(2400.0/float(DPI),1220.0/float(DPI))
	
	
	fig.autofmt_xdate()
	canvas=FigureCanvas(fig)
	response=HttpResponse(content_type='image/png')
	canvas.print_png(response)
	return response