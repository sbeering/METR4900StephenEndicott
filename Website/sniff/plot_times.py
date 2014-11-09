from pull_data import import_from_csv
from analyse import *
import MySQLdb as mysql
import csv
import os
import time, datetime

import matplotlib.pyplot as plt
from matplotlib.finance import quotes_historical_yahoo_ochl
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter

def plot_activity(values):

	daysFmt = DateFormatter("%d-%B %H:00")

	fig, ax = plt.subplots()

	times = values.keys()
	times.sort()
	number_found = [values[key] for key in times]

	ax.plot_date(times, number_found, '-')

	# format the ticks
	ax.xaxis.set_major_formatter(daysFmt)
	ax.autoscale_view()
	ax.grid(True)

	fig.autofmt_xdate()
	plt.show()

if __name__ == "__main__":
	found_devices = import_from_csv(os.path.join('D:\\','Dropbox','METR4900_Thesis','Analysis','offline_db.csv'))
	base_stations = load_base_stations('base_stations_24_hour.txt')
	start = datetime.datetime(2014,9,22,0)
	end = datetime.datetime(2014,9,26,0)
	count = count_minutes(found_devices,base_stations,start,end,resolution=5,stations=[0])
	plot_activity(count)