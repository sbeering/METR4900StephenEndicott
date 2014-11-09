#!/usr/bin/python
import os
import subprocess32 as subprocess

try:
    os.remove('/scripts/sniff.pid')
except:
    pass

tf = open('/config.json')
data = tf.read()
jdata = json.loads(data)

station_id = jdata['device']['id']
sniff = jdata['device']['wlan']

tf.close()
try:
	subprocess.call(["/usr/bin/airmon-ng","start",sniff], timeout = 3)
except:
	pass