#!/usr/bin/python

import sys, time, os, signal, pickle,subprocess, json, logging, MySQLdb, ConfigParser
from datetime import datetime
from daemon import Daemon
from scapy.all import *
from multiprocessing import Process
import mosquitto



kill_sniff = False

class MyDaemon(Daemon):



    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', 
        data='data.txt',output='signals.txt'):
        os.chdir("/scripts")
        
        tf = open('/config.json')
        data = tf.read()
        jdata = json.loads(data)

        tf.close()

        self.station_id = jdata['device']['id']
        self.sniff = jdata['device']['sniff']
        self.found_device_list = {}
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.datafile = data
        self.output = output

        self.host = ""
        self.user = ""
        self.password = ""
        self.database = ""

        self.db = MySQLdb.connect(self.host,self.user,self.password,self.database)

        logging.basicConfig(filename='logs/sniff.log',format=jdata['logging']['string_format'], datefmt=jdata['logging']['time_format'],level=jdata['logging']['level'])
        self.logger = logging.getLogger(__name__)

        
    def run(self):
        #self.hopper = Process(target = self.channel_hopper)
        #self.hopper.start()
        self.mqttc = mosquitto.Mosquitto()
        self.mqttc.connect("winter.ceit.uq.edu.au", 1883, 60)
        sniff(iface="mon0", prn = self.PacketHandler, stopperTimeout=1, stopper=self.stopperCheck, store=0)

    def stop(self):
        """
        Stop the daemon
        """
        global kill_sniff
        kill_sniff = True
        time.sleep(1)
        
        
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
 
        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart
        # Try killing the daemon process       
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

		
		
    def PacketHandler(self,pkt):
        try:
            self.cursor = self.db.cursor()
            self.cursor.execute("SELECT VERSION()")
        except:
            self.logger.warning("Connection to database lost. Reconnecting")
            self.db = MySQLdb.connect(self.host,self.user,self.password,self.database)
            self.cursor = self.db.cursor()

        if pkt.haslayer(Dot11):
            #Subtype 4 is a Probe Request
            if pkt.subtype in [4]:
                #Check for packet type. Subtype 8 = Beacon, 0 = Association Request, 4 = Probe request
                #print "Device: %s, Info: %s" %(pkt.addr2, pkt.info)
                if (pkt.addr2 != None):
                    MAC_address = pkt.addr2
                    #Check if it is a new device
                    if (MAC_address not in self.found_device_list.keys()) :
                        self.found_device_list[MAC_address] = [time.time()]
                        data = {'time':time.time(),'location':self.station_id,'address':MAC_address}



                        sql = "SELECT * FROM devices WHERE MAC_address = '%s'" % MAC_address
                        result = cursor.execute(sql)
                        if int(result) < 1:
                            sql = "INSERT INTO devices (MAC_address) VALUES ('%s')" % MAC_address
                            #Potential New
                            #sql = "INSERT INTO `steph154_thesis`.`devices` (`MAC_address`, `type`, `notes`, `owner`) VALUES ('%s', NULL, NULL, NULL);" % MAC_address

                            try:
                                result = cursor.execute(sql)
                                self.db.commit()
                                #print "Inserted device: %s" % MAC_address
                            except: 
                                #print "Failed to add device: %s" % MAC_address
                                # Rollback in case there is any error
                                self.db.rollback()
                                self.logger.error("Failed to post to database")

                        self.publish(data)

                            
                    elif (time.time() - self.found_device_list[MAC_address][-1]) > 30:
                        self.found_device_list[MAC_address].append(time.time())
                        #text = "Device: %s Frame Type %i Last seen %s seconds ago" %(pkt.addr2,pkt.subtype,(time.time() - self.found_device_list[pkt.addr2][-2]))
                        data = {'time':time.time(),'location':self.station_id,'address':MAC_address}
                        

                        self.publish(data)


            elif (pkt.addr2 != None) and (pkt.addr2 in self.found_device_list.keys()) and ((time.time() - self.found_device_list[pkt.addr2][-1]) > 30):
                    MAC_address = pkt.addr2
                    self.found_device_list[MAC_address].append(time.time())
                    #text = "Device: %s Frame Type %i Last seen %s seconds ago" %(pkt.addr2,pkt.subtype,(time.time() - self.found_device_list[pkt.addr2][-2]))
                    data = {'time':time.time(),'location':self.station_id,'address':MAC_address}

                    self.publish(data)


        try:
            cursor.close()
        except:
            pass
            
	
    def publish(self,data):
        jdata = json.dumps(data)
        self.logger.info(jdata)
        try:
            self.mqttc.publish("stephentest/sniff", jdata)
        except:
            self.logger.error("Failed to post to MQTT message %s" %jdata)
            #Add to a file to upload later when connection returns


        sql = "INSERT INTO found_devices (MAC_address,stations_id,time) VALUES ('%s','%d','%s')" %(MAC_address,self.station_id,time.time())

        try:
          result = self.cursor.execute(sql)
          self.db.commit()
          #print "Inserted device: %s" % MAC_address
        except: 
          #print "Failed to add device: %s" % MAC_address
          # Rollback in case there is any error
          self.db.rollback()
          self.logger.error("Failed to post to database")

    def stopperCheck(self):
        global kill_sniff
        
        #print "Check kill" 
        if kill_sniff: 

            # Time to stop the sniffer ;)
            #print "sniffer stopping"
            return True

        # No ? let's continu
        return False

						
						
if __name__ == "__main__":
    os.chdir('/scripts')
    cwd = os.getcwd() + '/'
    
    daemon = MyDaemon(cwd+'sniff.pid',cwd+'logs/daemon.log',cwd+'logs/daemon.log',cwd+'logs/daemonerr.log')


    
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
