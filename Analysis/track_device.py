from pull_data import import_from_csv
from analyse import *
import MySQLdb as mysql
import csv
import os
import time, datetime
import math
from plot_times import *

import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter




def track_devices(found_devices,base_stations,verbose=False):
	"""
	Track the stations devices passes through
	Input
		found_devices is a dictionary of instances in the format 
		e.g		found_devices[device_id] = {'mac_address':MAC,'station':station,'time':time} where device ID, is the database identifier
		base_stations is a list of base stations that should be ignored for the purpose of the analysis



	Options:
		verbose = print extended output

	"""

	devices = {}

	for key in found_devices.keys():
		found_time = time.localtime(float(found_devices[key]['time']))
		hour = datetime.datetime(found_time.tm_year,found_time.tm_mon,found_time.tm_mday,found_time.tm_hour)
		mac_address = found_devices[key]['mac_address']
		station = found_devices[key]['station']



		if mac_address not in base_stations:
			if mac_address not in devices.keys():
				devices[mac_address] = {'time':[hour],'stations':set()}
			else:
				devices[mac_address]['time'].append(hour)
			devices[mac_address]['stations'].add(station)

	for key in devices.keys():
		if len(devices[key]['time']) > 100:
			print "%s \t %s \t %s" %(key,len(devices[key]['time']),devices[key]['stations'])
	return devices

def device_values(mac_address,found_devices,start=datetime.datetime(2014,1,1,0),end=datetime.datetime(2015,1,1),resolution=1,verbose=False):
	"""
	Input
		mac_address is the mas address of the device being investigated
		found_devices is a dictionary of instances in the format 
		e.g		found_devices[device_id] = {'mac_address':MAC,'station':station,'time':time} where device ID, is the database identifier


	Output
		ount is a dictionary with the keys being datetime objects representing the hours, and the values being the number of devices found on that hour.
		e.g. 	count[datetime(2014,9,20,18)] = 34


	Options:
		verbose = print extended output

	"""
	count = {}

	stations = set()

	for key in found_devices.keys():
		found_time = time.localtime(float(found_devices[key]['time']))
		time_found = datetime.datetime(found_time.tm_year,found_time.tm_mon,found_time.tm_mday,int(math.floor((found_time.tm_hour/resolution)*resolution)))
		station = found_devices[key]['station']
		stations.add(station)

		if start <= time_found <= end and found_devices[key]['mac_address'] == mac_address:
			if time_found not in count:
				count[time_found] = {'stations':{}}
				if station not in count[time_found]['stations'].keys():
					count[time_found]['stations'][station] = 1
				else:
					count[time_found]['stations'][station] += 1

			else:
				if station not in count[time_found]['stations'].keys():
					count[time_found]['stations'][station] = 1
				else:
					count[time_found]['stations'][station] += 1

	start = min(count.keys())
	current = min(count.keys())
	end = max(count.keys())
	step = datetime.timedelta(hours=resolution)
	stations = list(stations)
	while current < end:
		if current not in count.keys():
			count[current] = {'stations':{}}

		

		

		current += step
	times = count.keys()
	times.sort()
	for current in times:
		for station in stations:
				if station not in count[current]['stations'].keys():
					count[current]['stations'][station] = 0
		
		print current,' ',count[current]['stations']

	return count


if __name__ == "__main__":
	device = 'f8:a9:d0:18:a6:b5'
	#device = 'd4:f4:6f:af:c9:d8'.lower()
	#Jess
	#device = '84:b1:53:77:58:4e'
	#Colby
	#device ='fe:80:a9:d0:42:2f:bb'
	#Louis
	#device = 'f8:a9:d0:56:cc:86'
	#Unknown
	#device = 'ac:22:0b:e3:b5:cf'
	#Justin
	#device = 'f8:a9:d0:4d:d4:f4'
	#Danial
	#device = '24:A2:E1:2B:01:D5'.lower()
	#Unknown
	#device = 'a6:c0:e1:de:b9:ee'
	start = datetime.datetime(2014,10,20,0)
	end = datetime.datetime(2014,11,3,0)
	#found_devices = import_from_csv(os.path.join('D:\\','Dropbox','METR4900_Thesis','Analysis','offline_db.csv'))
	found_devices = import_from_csv(os.path.join('offline_db.csv'))
	base_stations = load_base_stations('base_stations_24_hour.txt')
	device_values = device_values(device,found_devices,verbose=False,start=start,end=end)
	plot_device(device_values,device)
	#track_devices(found_devices,base_stations,verbose=False) 
