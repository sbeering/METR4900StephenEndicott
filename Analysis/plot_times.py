from pull_data import import_from_csv
from analyse import *
import MySQLdb as mysql
import csv
import os
import time, datetime

import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter,HourLocator,DayLocator

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 14}

plt.rc('font', **font)

def plot_activity(values,save=False,title='',x_label="",y_label="",resolution=24):

	daysFmt = DateFormatter("%d-%b %H:00")

	fig, ax = plt.subplots()

	times = values.keys()
	times.sort()

	number_found = [values[key] for key in times]

	ax.plot_date(times, number_found, '-')

	# format the ticks
	ax.xaxis.set_major_locator(DayLocator(bymonthday=range(1,32), interval=1))
	ax.xaxis.set_major_formatter(daysFmt)
	ax.autoscale_view()
	ax.grid(True)

	#ax.set_ylabel(x_label)
	#ax.set_ylabel(y_label)

	fig.autofmt_xdate()
	#plt.title(title)
	name = "base_station_noise_20th_oct-2nd_nov_station_0_%dhr_interval_5min_resolution.pdf" %resolution
	plt.savefig(name)
	plt.show()

def plot_device(values,mac_address='',title=''):

	daysFmt = DateFormatter("%d-%b %H:00")

	col = ['g','b','c','m','y','r']
	counter = 0

	fig, ax = plt.subplots()
	plt.hold(True)
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
	#ax.legend(loc='upper right')
	#plt.title(mac_address)
	plt.show()

def plot_noise_comparison(non_noise_values,noise_values,title='',resolution=24):

	daysFmt = DateFormatter("%d-%b %H:00")

	fig, ax = plt.subplots()

	noise_times = noise_values.keys()
	noise_times.sort()

	non_noise_times = non_noise_values.keys()
	non_noise_times.sort()

	noise_number_found = [noise_values[key] for key in noise_times]
	non_noise_number_found = [non_noise_values[key] for key in non_noise_times]

	ax.plot_date(noise_times, noise_number_found, '-',label='Including WAPs')
	ax.plot_date(non_noise_times, non_noise_number_found, '-',label='Excluding WAPs')

	# format the ticks
	ax.xaxis.set_major_locator(DayLocator(bymonthday=range(1,32), interval=1))
	ax.xaxis.set_major_formatter(daysFmt)
	ax.autoscale_view()
	ax.grid(True)


	#ax.legend(loc='upper right')

	fig.autofmt_xdate()
	#plt.title(title)
	name = "Noise_comparison_20th_Oct-2nd_Nov_%d_hour_resolution_base_station_0.pdf" %resolution
	plt.savefig(name)
	plt.show()

def plot_bar(values,save=False,title='',x_label="",y_label="",name=""):
	print values

	width = 0.35 

	daysFmt = DateFormatter("%d-%B %H:00")

	fig, ax = plt.subplots()

	times = values.keys()
	times.sort()

	number_found = [values[key] for key in times]

	ax.bar(times, number_found, width, color='r')

	ax.autoscale_view()
	ax.grid(True)
	#ax.set_ylabel(x_label)
	#ax.set_ylabel(y_label)

	fig.autofmt_xdate()
	#plt.title(title)
	if name:
		plt.savefig(name)

	plt.show()


if __name__ == "__main__":
	#found_devices = import_from_csv(os.path.join('D:\\','Dropbox','METR4900_Thesis','Analysis','offline_db.csv'))
	
	found_devices = import_from_csv(os.path.join('offline_db.csv'))
	
	WAPs = load_base_stations('base_stations_24_hour.txt')
	start = datetime.datetime(2014,10,20,0)
	end = datetime.datetime(2014,11,3,0)
	#Count excluding WAPS
	#count = count_minutes(found_devices,WAPs,start=start,end=end,stations=[0],resolution=15)
	
	#count = base_station_noise(found_devices,base_stations,start,end,stations=[0],resolution=5)
	#count = count_minutes(found_devices,[])

	#Count including WAPS
	count = count_minutes(found_devices,[],start=start,end=end,stations=[0],resolution=15)
	
	#count = daily_unique_devices(found_devices,WAPs,start=start,end=end,verbose=True)
	#plot_bar(count,save=False,title='',name='Daily_unique_deivces_oct23-nov3rd_station_0.pdf',x_label="Day",y_label="Number of Unique devices")

	plot_activity(count,title='October 20th - November 2nd activity profile\nStation 0 with WAPs',x_label="Time",y_label="Number of sniffs\nper 15 minutes")


	times = [6,12,18,24,36,48]
	"""
	for current_time in times:
		base_stations = load_base_stations('base_stations_'+str(current_time)+'_hour.txt')
		count = base_station_noise(found_devices,base_stations,start,end,stations=[0],resolution=5)

		#find_base_stations(found_devices,threshold=current_time,outfile='base_stations_'+str(current_time)+'_hour.txt')
		plot_activity(count,title="Base station noise 20th Oct - 2nd Nov, %d hour resolution at base station 0" %current_time,resolution=current_time)
	

	
	"""

	"""
	with_WAPs = count_minutes(found_devices,[],start,end,stations=[0],resolution=5)
	for current_time in times:
		WAPs = load_base_stations('base_stations_%d_hour.txt' %current_time)
		
		without_WAPs = count_minutes(found_devices,WAPs,start,end,stations=[0],resolution=5)
		plot_noise_comparison(without_WAPs,with_WAPs,title="Noise comparison 20th Oct - 2nd Nov %d hour resolution at base station 0\n" %current_time,resolution=current_time)
	
	
	"""
	"""
	current_time = 24
	WAPs = load_base_stations('base_stations_%d_hour.txt' %current_time)
	with_WAPs = count_minutes(found_devices,[],start,end,stations=[0],resolution=5)
	without_WAPs = count_minutes(found_devices,WAPs,start,end,stations=[0],resolution=5)
	plot_noise_comparison(without_WAPs,with_WAPs,title="Noise comparison 20th Oct - 2nd Nov %d hour resolution at base station 0\n" %current_time,resolution=current_time)
	"""
