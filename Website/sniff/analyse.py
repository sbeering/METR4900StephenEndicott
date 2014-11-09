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


def load_base_stations(file_path="thesis_data/base_stations_24_hour.txt"):
	devices = []
	fp = open(os.path.join(settings.STATIC_ROOT, file_path), 'r+')
	#fp = open('base_stations_24_hour.txt', 'r+')
	#fp = urlopen('http://stephenendicott.info/static/thesis_data/base_stations_24_hour.txt')
	data = fp.read().splitlines()
	for line in data:
		devices.append(line.encode("utf8"))


	return data
	

def get_found_devices(start_date=None,end_date=None,base_stations=[]):


	if not start_date:
		start_date = datetime.datetime(2014,1,1,0,0)
	if not end_date:
		end_date = datetime.datetime(2015,1,1,0,0)
	
	start_unix = int(start_date.strftime('%s'))
	end_unix = int(end_date.strftime('%s'))

	django_devices = FoundDevices.objects.filter(time__range=(start_unix, end_unix)).exclude(mac_address__in=base_stations).values()
	
	found_devices = {}
	for entry in django_devices:
		found_devices[entry['found_id']] = {'mac_address':entry['mac_address'].encode("utf8"),'station':str(entry['stations_id']),'time':entry['time'].encode("utf8")}
	
	


	return found_devices

def count_minutes(found_devices,base_stations,start=datetime.datetime(2014,1,1),end=datetime.datetime(2015,1,1),resolution=15,stations=range(10),verbose=False):
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
				if minute not in minute_count.keys():
					minute_count[minute] = 1

				else:
					minute_count[minute] += 1


	for key,value in minute_count.items():
		if verbose:
			print key.strftime('%Y-%m-%d %H:%M'),': ',value
	key  = found_devices.keys()[6]
	#print minute_count.keys()
	#assert 0, '%s\t%s\t%s\t%s'%(len(found_devices),found_devices[key],len(base_stations),len(minute_count))
	return minute_count
	
	

def import_from_csv(file_path="thesis_data/offline_db.csv"):

	found_devices = {}
	#fp = urlopen('http://stephenendicott.info/static/thesis_data/offline_db.csv')
	fp = open(os.path.join(settings.STATIC_ROOT, file_path), 'r+')
	#with open(os.path.join(settings.STATIC_ROOT, file_path), 'r+') as csvfile:
	with fp as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		next(reader)
		
		for row in reader:
			device_id = row[0]
			MAC = row[1]
			station = row[2]
			time = row[3]
			found_devices[device_id] = {'mac_address':MAC,'station':station,'time':time}

	return found_devices
	
	
	
def device_values(mac_address,base_stations=[],start=datetime.datetime(2014,1,1,0),end=datetime.datetime(2015,1,1),resolution=1,verbose=False,start_date=None,end_date=None):
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
	if not start_date:
		start_date = datetime.datetime(2014,1,1,0,0)
	if not end_date:
		end_date = datetime.datetime(2015,1,1,0,0)
	
	start_unix = int(start_date.strftime('%s'))
	end_unix = int(end_date.strftime('%s'))
	
	django_devices = FoundDevices.objects.filter(time__range=(start_unix, end_unix),mac_address=mac_address).exclude(mac_address__in=base_stations).values()
	
	found_devices = {}
	for entry in django_devices:
		found_devices[entry['found_id']] = {'mac_address':entry['mac_address'].encode("utf8"),'station':str(entry['stations_id']),'time':entry['time'].encode("utf8")}
	
	


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
	
	
def track_shift(times,found_devices,shift_station,start,base_stations=[],verbose=False):

	print 'Number of entries to analyse: ',len(found_devices)
	#devices[mac_address] = {'inside':inside_time_frame_count,'outside':outside_time_frame_count}
	week_start = start
	week_end = start + datetime.timedelta(days=7)
	devices = {}

	stop = len(found_devices.keys())/10
	counter = 0
	number = 0

	for key in [x for x in found_devices.keys() if found_devices[x]['mac_address'] not in base_stations]:


		if verbose:
			counter += 1
			if counter == stop:
				counter = 0
				number += 10
				print "%d%%" %number
		mac_address = found_devices[key]['mac_address']
		station = found_devices[key]['station']

		if mac_address != '8:a9:d0:18:a6:b5':

			found_time = time.localtime(float(found_devices[key]['time']))
			dt = datetime.datetime(found_time.tm_year,found_time.tm_mon,found_time.tm_mday,found_time.tm_hour,found_time.tm_min)

			during_shift = False
			during_day = False

			if (mac_address not in base_stations) and (station == shift_station):

				if week_start <= dt <= week_end:
					if mac_address not in devices.keys():
						devices[mac_address] = {'inside':0,'outside':0,'ratio':0,'score':0,'total':0,'times':[],'start_score':0}
					for shift in times:
						day_start = datetime.datetime(shift[0].year,shift[0].month,shift[0].day)
						day_end = datetime.datetime(shift[1].year,shift[1].month,shift[1].day) + datetime.timedelta(days=1)
						if day_start <= dt <= day_end:
							during_day = True
							devices[mac_address]['times'].append(dt)
							if shift[0] <= dt <= shift[1]:
								during_shift = True
					if during_shift:
						devices[mac_address]['inside'] += 1
					elif during_day:
						devices[mac_address]['outside'] += 1
					else:
						devices[mac_address]['outside'] += .5


	for mac_address in devices.keys():
		devices[mac_address]['ratio'] = float(devices[mac_address]['inside'])/(float(devices[mac_address]['outside']+1.0))
		total = (float(devices[mac_address]['inside'])+(float(devices[mac_address]['outside']+1.0)))
		devices[mac_address]['score'] = devices[mac_address]['ratio'] * math.sqrt(total)
		devices[mac_address]['start_score'] = devices[mac_address]['ratio'] * math.sqrt(total)
		devices[mac_address]['total'] = total

		delta = datetime.timedelta(minutes=60)
		step = delta/2
			
		for shift in times:
			

			current = shift[0] - step
			#print 'Shift Start: ',shift[0],'\tShift End',shift[1]
			while current <= shift[1]:
				
				found = False
				#print 'Start bracket: ',current,'\tEnd Bracket: ',(current + delta)
				for entry in devices[mac_address]['times']:
					if current <= entry <= (current + delta):
						#print 'Within Mac: ',mac_address,'\tShift Start: ',shift[0],'\tShift End: ',shift[1],'\tCurrent: ',current,'\tEntry: ',entry,'\tCurrent+Delta: ',(current + delta)
						found = True
					else:
						pass
						#print 'Outside Mac: ',mac_address,'\tShift Start: ',shift[0],'\tShift End: ',shift[1],'\tCurrent: ',current,'\tEntry: ',entry,'\tCurrent+Delta: ',(current + delta)
				current += step
			
		

				if found == False:
					#print 'Modifying score Start: ',current,'\tEntry: ',entry,'\tEnd: ',(current + delta)
					devices[mac_address]['score'] = devices[mac_address]['score'] * .85
				

	final = sorted(devices.iteritems(), key=lambda x: x[1]['score'])
	final = [x for x in final if x[1]['total'] >= 15 and  x[1]['ratio'] > 2.5 and x[0] not in base_stations]
	final.reverse()

	if len(final) < 20:
		count = len(final)
	else:
		count = 20
		
	

	for num in range(count):
		final[num][1]['num'] = num +1
		mac_address = final[num][0]
		ratio = final[num][1]['ratio']
		inside = final[num][1]['inside']
		outside = final[num][1]['outside'] 
		total = final[num][1]['inside'] + final[num][1]['outside'] 
		score = final[num][1]['score']
		start_score = final[num][1]['start_score']
		
	return final[:count]