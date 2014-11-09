from pull_data import import_from_csv, import_from_db
import MySQLdb as mysql
import csv
import os
import time, datetime
import math

import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter

def count_hours(found_devices,base_stations=[],start=datetime.datetime(2014,1,1,0),end=datetime.datetime(2015,1,1),verbose=False):
	"""
	Input
		found_devices is a dictionary of instances in the format 
		e.g		found_devices[device_id] = {'mac_address':MAC,'station':station,'time':time} where device ID, is the database identifier
		base_stations is a list ofbase stations to be ignored


	Output
		hour_count is a dictionary with the keys being datetime objects representing the hours, and the values being the number of devices found on that hour.


	Options:
		verbose = print extended output

	"""


	hour_count = {}

	for key in found_devices.keys():
		if found_devices[key]['mac_address'] not in base_stations:
			found_time = time.localtime(float(found_devices[key]['time']))
			hour = datetime.datetime(found_time.tm_year,found_time.tm_mon,found_time.tm_mday,found_time.tm_hour)
			if start <= minute <= end and found_devices[key]['station'] == '0':
				if hour not in hour_count:
					hour_count[hour] = 1

				else:
					hour_count[hour] += 1


	for key,value in hour_count.items():
		if verbose:
			print key.strftime('%Y-%m-%d %H:00'),': ',value

	return hour_count

def count_minutes(found_devices,base_stations,start=datetime.datetime(2014,1,1,0),end=datetime.datetime(2015,1,1),resolution=15,stations=range(10),verbose=False):
	"""
	Input
		found_devices is a dictionary of instances in the format 
		e.g		found_devices[device_id] = {'mac_address':MAC,'station':station,'time':time} where device ID, is the database identifier
		base_stations is a list ofbase stations to be ignored


	Output
		minute_count is a dictionary with the keys being datetime objects representing the hours, and the values being the number of devices found on that hour.
		e.g. 	minute_count[datetime(2014,9,20,18)] = 34


	Options:
		verbose = print extended output

	"""

	stations_int = list(stations)
	stations = [str(station) for station in stations_int]


	minute_count = {}

	for key in found_devices.keys():
		if found_devices[key]['mac_address'] not in base_stations:
			found_time = time.localtime(float(found_devices[key]['time']))
			minute = datetime.datetime(found_time.tm_year,found_time.tm_mon,found_time.tm_mday,found_time.tm_hour,int(math.floor((found_time.tm_min/resolution)*resolution)))
			if start <= minute <= end and found_devices[key]['station'] in stations:
				if minute not in minute_count:
					minute_count[minute] = 1

				else:
					minute_count[minute] += 1


	for key,value in minute_count.items():
		if verbose:
			print key.strftime('%Y-%m-%d %H:%M'),': ',value
	#print minute_count.keys()
	return minute_count


def base_station_noise(found_devices,base_stations,start=datetime.datetime(2014,1,1,0),end=datetime.datetime(2015,1,1),resolution=15,stations=range(10),verbose=False):
	"""
	Input
		found_devices is a dictionary of instances in the format 
		e.g		found_devices[device_id] = {'mac_address':MAC,'station':station,'time':time} where device ID, is the database identifier
		base_stations is a list ofbase stations to be ignored


	Output
		minute_count is a dictionary with the keys being datetime objects representing the hours, and the values being the number of devices found on that hour.
		e.g. 	minute_count[datetime(2014,9,20,18)] = 34


	Options:
		verbose = print extended output

	"""

	stations_int = list(stations)
	stations = [str(station) for station in stations_int]


	minute_count = {}

	for key in found_devices.keys():
		if found_devices[key]['mac_address'] in base_stations:
			found_time = time.localtime(float(found_devices[key]['time']))
			minute = datetime.datetime(found_time.tm_year,found_time.tm_mon,found_time.tm_mday,found_time.tm_hour,int(math.floor((found_time.tm_min/resolution)*resolution)))
			if start <= minute <= end and found_devices[key]['station'] in stations:
				if minute not in minute_count:
					minute_count[minute] = 1

				else:
					minute_count[minute] += 1


	for key,value in minute_count.items():
		if verbose:
			print key.strftime('%Y-%m-%d %H:%M'),': ',value
	#print minute_count.keys()
	return minute_count

def find_base_stations(found_devices,threshold=24,outfile=False,verbose=False):
	"""
	If a device is found at least once an hour for 48 hours it is considered to be a base _station and should not be considered in further analysis

	Input
		found_devices is a dictionary of instances in the format 
		e.g		found_devices[device_id] = {'mac_address':MAC,'station':station,'time':time} where device ID, is the database identifier


	Output
		base_stations is a list of mac addresses of devices that are not client devices. Includes routers sending out probe requests
		e.g 	[device1,device2......]


	Options:
		verbose = print extended output

	"""
	base_stations = set()
	devices = {}

	if verbose:
		print "Starting entry analysis. Total entires %d" %len(found_devices.keys())

	stop = len(found_devices.keys())/10
	counter = 0
	number = 0
	for key in found_devices.keys():
		if verbose:
			counter += 1
			if counter == stop:
				counter = 0
				number += 10
				print "%d%%" %number


		mac = found_devices[key]['mac_address']
		found_time = time.localtime(float(found_devices[key]['time']))
		if mac not in devices.keys():
			devices[mac] = set()
			devices[mac].add(datetime.datetime(found_time.tm_year,found_time.tm_mon,found_time.tm_mday,found_time.tm_hour))
		else:
			devices[mac].add(datetime.datetime(found_time.tm_year,found_time.tm_mon,found_time.tm_mday,found_time.tm_hour))


	if verbose:
		print "Starting device analysis. Total devices %d" %len(devices.keys())

	stop = len(devices.keys())/10
	counter = 0
	number = 0
	for mac in devices.keys():

		if verbose:
			counter += 1
			if counter == stop:
				counter = 0
				number += 10
				print("%d%%" %number)
		#Iterate over list of found time
		times = list(devices[mac])
		times.sort()
		if len(times) > 12:
			count = 0 
			for i in range(len(times) - 1)[::-1]:
				if int((times[i+1]-times[i]).total_seconds()) == 3600:
					count += 1
				else:
					count = 0
				if count >= threshold:
					base_stations.add(mac)


	if outfile:
		fp = open(outfile,'w+')
		for device in list(base_stations):
			fp.write('%s\n' %device)
		fp.close()

	return list(base_stations)

def load_base_stations(file_path):
	devices = []
	fp = open(file_path,'r+')
	data = fp.read().splitlines()
	for line in data:
		devices.append(line)


	return data


def daily_unique_devices(found_devices,WAPs=[],stations=['0'],start=datetime.datetime(2014,1,1,0),end=datetime.datetime(2015,1,1),verbose=False):
	"""
	Input
		found_devices is a dictionary of instances in the format 
		e.g		found_devices[device_id] = {'mac_address':MAC,'station':station,'time':time} where device ID, is the database identifier
		WAPs is a list ofbase stations to be ignored


	Output
		hour_count is a dictionary with the keys being datetime objects representing the hours, and the values being the number of devices found on that hour.


	Options:
		verbose = print extended output

	"""


	day_devices = {}

	for key in found_devices.keys():
		if found_devices[key]['mac_address'] not in WAPs:
			found_time = time.localtime(float(found_devices[key]['time']))
			day = datetime.datetime(found_time.tm_year,found_time.tm_mon,found_time.tm_mday)
			if start <= day <= end and found_devices[key]['station'] in stations:
				if day not in day_devices:
					day_devices[day] = set(found_devices[key]['mac_address'])

				else:
					day_devices[day].add(found_devices[key]['mac_address'])

	day_count = {}

	for key,value in day_devices.items():
		day_count[key] = len(value)


	for key,value in day_count.items():
		if verbose:
			print key.strftime('%Y-%m-%d'),': ',value

	return day_count

if __name__ == "__main__":
	#found_devices = import_from_csv(os.path.join('D:\\','Dropbox','METR4900_Thesis','Analysis','offline_db.csv'))
	found_devices = import_from_csv(os.path.join('offline_db.csv'))
	#found_devices = import_from_db()
	#hour_count = count_hours(found_devices,verbose=True)
	#find_base_stations(found_devices,threshold=18,outfile='base_stations_18_hour.txt',verbose=True)
	WAPs = load_base_stations('base_stations_24_hour.txt')
	

	times = [6,12,18,36,48]

	"""
	for current_time in times:
		find_base_stations(found_devices,threshold=current_time,outfile='base_stations_'+str(current_time)+'_hour.txt')
	"""
	daily_unique_devices(found_devices,WAPs,start=datetime.datetime(2014,10,20,0),end=datetime.datetime(2014,11,3),verbose=True)
