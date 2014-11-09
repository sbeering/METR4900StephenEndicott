import MySQLdb as mysql
import csv
import os




"""
Returns a dictionary version of thie folloing table
|---------------------|---------------------|---------------------|---------------------|---------------------|
|Found_ID             |MAC_Address          |Station ID           |Time Found           |                     |
|---------------------|---------------------|---------------------|---------------------|---------------------|
|0                    |00-16-ea-b5-a3-3e    |1                    |141246295.535        |                     |
|1                    |00-16-ea-b5-a3-3e    |1                    |1412462996.545       |                     |
|2                    |00-16-ea-b5-a3-3e    |2                    |14124629346.835      |                     |
|3                    |20-36-e3-75-b3-8e    |3                    |1412464396.895       |                     |
|4                    |00-16-ea-b5-a3-3e    |3                    |14124628796.235      |                     |
|5                    |05-13-ba-25-34-ce    |1                    |1412445996.13        |                     |


"""



def import_from_db(outfile=False):

	if outfile:
		out = open(outfile,'wb')
		out.write("id,mac_address,station,time\n")
		#writer = csv.writer(out, delimiter=',')



	found_devices = {}
	# Open database connection
	db = mysql.connect()

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# Prepare SQL query to INSERT a record into the database.
	sql = "SELECT * FROM found_devices"


	try:
		# Execute the SQL command
		cursor.execute(sql)
		# Fetch all the rows in a list of lists.
		results = cursor.fetchall()

		for row in results:
			device_id = row[0]
			MAC = row[1]
			station = row[2]
			time = row[3]
			found_devices[device_id] = {'mac_address':MAC,'station':station,'time':time}


			if outfile:
				out.write("%s,%s,%s,%s\n" %(device_id,MAC,station,time))
				#writer.writerow(device_id,MAC,station,time)



		
	except:
		print "Error: unable to fecth data"



	print "Total results: %d" %len(found_devices.keys())
	# disconnect from server
	db.close()
	if outfile:
		out.close()

	return found_devices


def import_from_csv(infile):

	found_devices = {}

	with open(infile, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		next(reader)
		
		for row in reader:
			device_id = row[0]
			MAC = row[1]
			station = row[2]
			time = row[3]
			found_devices[device_id] = {'mac_address':MAC,'station':station,'time':time}

	return found_devices


if __name__ == "__main__":
	#found_devices['id'] = {'mac_address':MAC,'station':station,'time':time} 
	#import_from_db(outfile='offline_db.csv')
	found_devices = import_from_db('offline_db.csv')