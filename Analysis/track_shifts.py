from pull_data import import_from_csv
from analyse import *
import MySQLdb as mysql
import csv
import os
import time, datetime
import math

import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter


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
			



				


	print 'Number of devices found: ',len(devices)
	final = sorted(devices.iteritems(), key=lambda x: x[1]['score'])
	final = [x for x in final if x[1]['total'] >= 15 and  x[1]['ratio'] > 2.5 and x[0] not in base_stations]
	final.reverse()

	if len(final) < 20:
		count = len(final)
	else:
		count = 20

	for num in range(count):
		mac_address = final[num][0]
		ratio = final[num][1]['ratio']
		inside = final[num][1]['inside']
		outside = final[num][1]['outside'] 
		total = final[num][1]['inside'] + final[num][1]['outside'] 
		score = final[num][1]['score']
		start_score = final[num][1]['start_score']
		print num+1,' Device: ',mac_address,'\tInside: ',inside,'\tOutside: ',outside,'\tRatio: ',ratio,'\tTotal: ',total,'\tScore: ',score,'\tStart Score: ',start_score








if __name__ == "__main__":
	station = 0	
	start = datetime.datetime(2014,10,20,0,0)
	
	#Louis Times - Week begining 8th september
	#times = [(datetime.datetime(2014,9,9,9,0),datetime.datetime(2014,9,9,17,0)),(datetime.datetime(2014,9,10,9,0),datetime.datetime(2014,9,10,17,0)),(datetime.datetime(2014,9,11,9,0),datetime.datetime(2014,9,11,9,17))]
	
	#Louis Week begining 20th October
	#times = [(datetime.datetime(2014,10,21,9,0),datetime.datetime(2014,10,21,17,0)),(datetime.datetime(2014,10,22,9,0),datetime.datetime(2014,10,22,17,0)),(datetime.datetime(2014,10,23,9,0),datetime.datetime(2014,9,23,17,0))]	
	
	#Louis Week begining 22nd september
	#times = [(datetime.datetime(2014,9,23,9,0),datetime.datetime(2014,9,23,17,0)),(datetime.datetime(2014,9,24,9,0),datetime.datetime(2014,9,24,17,0)),(datetime.datetime(2014,9,25,9,0),datetime.datetime(2014,10,25,17,0))]	
	

	#Stephen Times Week Beginning 6th October
	#times = [(datetime.datetime(2014,10,7,9,0),datetime.datetime(2014,10,7,17,0)),(datetime.datetime(2014,10,8,9,30),datetime.datetime(2014,10,8,18,0)),(datetime.datetime(2014,10,10,9,0),datetime.datetime(2014,10,10,16,30))]
	
	#Brett Times - Week begining 8th september
	#times = [(datetime.datetime(2014,9,11,8,0),datetime.datetime(2014,9,11,16,0)),(datetime.datetime(2014,9,12,8,0),datetime.datetime(2014,9,12,16,0)),(datetime.datetime(2014,9,13,8,0),datetime.datetime(2014,9,13,12,0))]
	#Brett Times - Week beginning 29th September
	#times = [(datetime.datetime(2014,10,3,10,0),datetime.datetime(2014,10,3,18,0)),(datetime.datetime(2014,10,4,8,0),datetime.datetime(2014,10,4,12,0))]
	#Brett Times - Week beginning 6th October
	#times = [(datetime.datetime(2014,10,9,10,0),datetime.datetime(2014,10,9,18,0)),(datetime.datetime(2014,10,10,10,0),datetime.datetime(2014,10,10,18,0)),(datetime.datetime(2014,10,11,8,0),datetime.datetime(2014,10,11,12,0))]
	
	#Colby Times Week Beginning 6th October
	#times = [(datetime.datetime(2014,10,7,9,45),datetime.datetime(2014,10,7,18,0)),(datetime.datetime(2014,10,9,12,45),datetime.datetime(2014,10,9,18,0))]
	
	#Lauretta -Times Week Beginning 6th October
	#times = [(datetime.datetime(2014,10,7,7,45),datetime.datetime(2014,10,7,16,0)),(datetime.datetime(2014,10,10,7,45),datetime.datetime(2014,10,10,16,0))]
	#Lauretta -Times Week Beginning 22nd September
	#times = [(datetime.datetime(2014,9,22,8,0),datetime.datetime(2014,9,22,16,0)),(datetime.datetime(2014,9,23,8,0),datetime.datetime(2014,9,23,16,0)),(datetime.datetime(2014,9,24,8,0),datetime.datetime(2014,9,24,16,0))]
	#found_devices['id'] = {'mac_address':MAC,'station':station,'time':time} 
	
	#Jess - Times Week Beginning 22nd September
	#times = [(datetime.datetime(2014,9,22,9,0),datetime.datetime(2014,9,22,17,0)),(datetime.datetime(2014,9,24,8,0),datetime.datetime(2014,9,24,16,0)),(datetime.datetime(2014,9,25,8,0),datetime.datetime(2014,9,25,16,0))]
	
	#Jess - Week begining 20th October
	times = [(datetime.datetime(2014,10,20,10,0),datetime.datetime(2014,10,20,15,0)),(datetime.datetime(2014,10,21,8,0),datetime.datetime(2014,10,21,16,0)),(datetime.datetime(2014,10,22,8,0),datetime.datetime(2014,10,22,16,0)),(datetime.datetime(2014,10,23,8,0),datetime.datetime(2014,9,23,13,0))]	
	

	#Danial - Week begining 22nd september
	#times = [(datetime.datetime(2014,9,22,8,0),datetime.datetime(2014,9,22,16,0)),(datetime.datetime(2014,9,24,8,0),datetime.datetime(2014,9,24,16,0)),(datetime.datetime(2014,9,25,8,0),datetime.datetime(2014,9,25,16,0))]

	#Justin - Week begining 22nd september
	#times = [(datetime.datetime(2014,9,22,8,0),datetime.datetime(2014,9,22,16,0)),(datetime.datetime(2014,9,23,8,0),datetime.datetime(2014,9,23,16,0)),(datetime.datetime(2014,9,24,8,0),datetime.datetime(2014,9,24,16,0))]
	#Justin- Week begining 8th september
	#times = [(datetime.datetime(2014,9,9,8,0),datetime.datetime(2014,9,9,16,0)),(datetime.datetime(2014,9,10,8,0),datetime.datetime(2014,9,10,16,0)),(datetime.datetime(2014,9,11,8,0),datetime.datetime(2014,9,11,16,0))]
	#Justin - Week begining 13th October
	#times = [(datetime.datetime(2014,10,14,8,0),datetime.datetime(2014,10,14,16,0)),(datetime.datetime(2014,10,15,8,0),datetime.datetime(2014,10,15,16,0)),(datetime.datetime(2014,10,16,8,0),datetime.datetime(2014,10,16,16,0)),(datetime.datetime(2014,10,17,10,0),datetime.datetime(2014,10,17,18,0))]

	#Mark - Week begining 22nd september
	#times = [(datetime.datetime(2014,9,22,8,0),datetime.datetime(2014,9,22,12,0)),(datetime.datetime(2014,9,23,8,0),datetime.datetime(2014,9,23,12,0)),(datetime.datetime(2014,9,25,8,0),datetime.datetime(2014,9,25,12,0))]

	#Chris - Week begining 22nd september
	#times = [(datetime.datetime(2014,9,24,9,0),datetime.datetime(2014,9,24,17,0)),(datetime.datetime(2014,9,25,9,0),datetime.datetime(2014,9,25,17,0))]

	#found_devices = import_from_csv(os.path.join('D:\\','Dropbox','METR4900_Thesis','Analysis','offline_db.csv'))
	found_devices = import_from_csv(os.path.join('offline_db.csv'))
	base_stations = load_base_stations('base_stations_24_hour.txt')


	track_shift(times,found_devices,'0',start,verbose=True)