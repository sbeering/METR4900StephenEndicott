#!/usr/bin/env python
import urllib,urllib2,socket,json, logging, os, sys, time, signal
from netifaces import interfaces, ifaddresses, AF_INET

def main(url='http://thesis.stephenendicott.com.au/script.php'):

    tf = open('/config.json')
    data = tf.read()
    jdata = json.loads(data)

    tf.close()

    logging.basicConfig(filename='/scripts/ip.log',format=jdata['logging']['string_format'], datefmt=jdata['logging']['time_format'],level=jdata['logging']['level'])
    logger = logging.getLogger(__name__)
    name = "Thesis_pi_" + str(jdata['device']['id'])
    info = ifaddresses(jdata['device']['wlan'])
    ip_pub =  urllib2.urlopen('http://ip.42.pl/raw').read()
    ip_int = info[2][0]['addr']
    #ip_int = socket.gethostbyname(socket.gethostname())

    values = {'ip_pub' : ip_pub,
                      'ip_int' : ip_int,
                      'secretstring':'I am so awesome',
                      'name':name}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    page = response.read()
    if page != 'Success':
            logger.info("Script did not exicute correctly")
    else:
            jdata = json.dumps({'public':ip_pub,'internal':ip_int})
            logger.info(jdata)

if __name__ == "__main__":
    main()

