# -*- coding: iso-8859-15 -*-
# $Id: pys60gps.py 245 2006-02-05 20:37:30Z arista $
# Copyright Aapo Rista 2005-2006

# pys60 modules
import appuifw
import e32
import sysinfo
import location
from key_codes import *
from graphics import *
# native python 2.2 modules
import math
import time
import random
import thread
import httplib
# own modules
import Logger
from Position import *
from BtGpsReader import *
from NMEAParser import *
from KKJWGS84 import *
from Calculate import *
from Track import *

class pys60gps:

    id = u'$Id: pys60gps.py 245 2006-02-05 20:37:30Z arista $' # DO NOT modify Id-string

    def __init__(self):
        # Enable logging into a file
        logfile = u"e:/pys60gps-%s-debug.log" % (time.strftime("%Y%m"))
        print u"Errorlog will be written to"
        print logfile
        my_log = Logger.Logger(logfile)
        sys.stderr = sys.stdout = my_log
        try: # Parse revision and last change date
            ida = self.id.split(" ")
            self.revision = ida[2]
            self.lastchangeddate = ida[3]
        except:
            self.revision = u'undefined'
            self.lastchangeddate = u'undefined'
        self.initialram = int(sysinfo.free_ram())/1024
        self.color = (64,128,64)
        self.app_running = 1
        self.screen_num = 0
        self.speedlimit = 40
        self.screen_update_delay = 0.2
        # Perhaps we need some kind of "screen class"?
        self.screens = (u'TECH', u'POSITION', u'DISTANCE', u'SPEED')
        self.fieldcolor = (0,0,32)        
        self.state = 'init'
        self.initialram = 0
        self.redraws = 0
        self.useragent = "positio.rista.net/en/pys60gps"
        self.useragent = "%s %s-rev-%s" % (self.useragent, self.lastchangeddate, self.revision)
        self.fetch_pois_running = False        
        self.poifilename = u'e:/pys60gps-poi.csv'        
        self.next_sortaction_time = time.time()
        self.next_savetrackpoint_time = time.time()
        self.next_sortaction_delay = 10 # seconds
        # gpsapp stuff start
        self.pos = Position() # Create datastore object for position data
        self.pos.line = u"NOTE:  Remember to select       Connect to GPS!"
        self.parser = NMEAParser(self.pos) # Create parser for NMEA sentences
        self.btr = BtGpsReader() # Create bluetooth gps reader
        self.read_gps_running = False
        # thread.start_new_thread(self.read_gps,()) # Start reading gpsbtgpsreader
        # gpsapp stuff end
        self.track = Track()
        self.calc = Calculate()
        self.pois = []
        self.pois.append([0, -1, u'Lasipalatsi', 60.169997, 24.937452])
        self.pois.append([0, -1, u'Näsinneula',  61.504952, 23.743258])
        self.pois.append([0, -1, u'Eiffel',      48.858,     2.295])
        self.pois.append([0, -1, u'Trafalgar',   51.50778,   0.12806])

        self.old_body = appuifw.app.body
        self.canvas = appuifw.Canvas(redraw_callback=self.redraw)
        self.draw = Draw(self.canvas)
        appuifw.app.body = self.canvas
        # Bind left and right arrows to screen switcher
        self.canvas.bind(EKeyRightArrow,lambda:self.switch_screen(1))
        self.canvas.bind(EKeyLeftArrow,lambda:self.switch_screen(-1))
        #self.canvas.bind(EKeyUpArrow,lambda:self.switch_screen(1))
        #self.canvas.bind(EKeyDownArrow,lambda:self.switch_screen(3))
        self.state='app_running'
        self.redraw(())

    def read_gps(self):
        """Read gps constantly while app is running."""
        self.read_gps_running = True
        status, msg = self.btr.connect()
        # (btaddr,services) = self.btr.target
        while self.app_running:
            try:
                status, NMEAline = self.btr.readline()
                self.pos.line = NMEAline
                if NMEAline is not None and NMEAline is not "":
                    self.parser.parse_line(NMEAline)
            except:
                self.btr.disconnect()
                return
            if self.pos.gpsstatus is "A" and self.next_savetrackpoint_time < time.time() and self.pos.get_age() >= 0 and self.pos.get_age() < 3:
                self.track.push([self.pos.lat, self.pos.lon,0, self.pos.getGpsUtcTime()])
                self.next_savetrackpoint_time = time.time() + 5
                pass
        self.btr.disconnect()
        self.read_gps_running = False
        print self.track

    def save_logs(self):
        """Write coordinates, old cellid and new cellid into logfile when gsm-cellid changes.
        We can later use these coordinates to map gsm-cells."""
        filename = u"e:/pys60gps-%s-cellid.log" % (time.strftime("%Y-%W"))
        old_cell = "%s,%s,%s,%s" % (location.gsm_location())
        old_cell = "0,0,0,0"
        while self.app_running:
            # Save cellid changes
            new_cell = "%s,%s,%s,%s" % (location.gsm_location())
            if old_cell != new_cell and self.pos.get_age() >= 0 and self.pos.get_age() < 3:
                speed = self.pos.speed_kmph
                course = self.pos.course
                logline = "%.6f;%.6f;%s;%s;%s;%s\n" % (self.pos.lat, self.pos.lon, old_cell, new_cell, speed, course)
                try:
                    f = open(filename,'a')
                    f.write(logline)
                    f.close()
                except:
                    print "Error writing %s to %s" (logline, filename)
                old_cell = new_cell
            e32.ao_sleep(0.5)

    def fetch_pois_from_gpswaypointsnet(self):
        self.fetch_pois_running = True
        params = ""
        headers = {"User-Agent": self.useragent}
        host = "www.gps-waypoints.net"
        url = "/gps/get_closest_waypoints.php?lat=%f&lon=%f&limit=100" % (self.pos.lat, self.pos.lon)
        self.userconn = httplib.HTTPConnection(host)
        self.userconn.request("GET", url, params, headers)
        response = self.userconn.getresponse()
        pois = response.read()
        f = open(self.poifilename,'w')
        f.write(pois)
        f.close()
        self.read_pois()
        self.fetch_pois_running = False
        
    def read_pois(self):
        try:
            f = open(self.poifilename,'r')
        except:
            errmsg = u"Error opeing file %s" % self.poifilename
            print errmsg
            appuifw.note(errmsg, 'info')
            return
        p = []
        dist = 0.0   # initial dist
        bearing = -1 # and bearing values
        for line in f:
            if line[0] != "#":
                try:
                    fields = line.split(",")
                    name = fields[2]
                    name = unicode(name,'latin-1')
                    p.append([dist, bearing, name, float(fields[0]), float(fields[1])])
                except:
                    pass
        self.pois = p
        self.sort_by_distance()
            
    def switch_screen(self,screen_num):
        self.screen_num = self.screen_num + screen_num
        if self.screen_num < 0:
            self.screen_num = len(self.screens) - 1
        elif self.screen_num >= len(self.screens):
            self.screen_num = 0
        
    def close_canvas(self): # break reference cycles
        appuifw.app.body = self.old_body
        self.canvas = None
        self.draw = None
        appuifw.app.exit_key_handler = None
        
    def redraw(self,rect):
        """Draw current screen."""
        self.redraws += 1
        if self.screen_num is 0:
            self.screen_update_delay = 0.2
            self.draw.clear(self.fieldcolor)
            self.draw_tech()
        elif self.screen_num is 1:
            self.screen_update_delay = 0.2
            self.draw.clear(self.fieldcolor)
            self.draw_position()
        elif self.screen_num is 2:
            self.screen_update_delay = 1.0
            self.draw.clear(self.fieldcolor)
            self.draw_distance()
        elif self.screen_num is 3:
            self.screen_update_delay = 0.2
            # cleared in the function
            self.draw_speed()

    def draw_tech(self):
        currentram = int(sysinfo.free_ram())/1024
        line = 14
        lineheight = 14
        self.draw.text((0,line),u"SYSTEM+GPS: %d redraws" % (self.redraws),(192,192,192))
        line = line + lineheight
        self.draw.text((0,line),u"Init RAM: %d kB" % (self.initialram),(192,192,192))
        line = line + lineheight
        self.draw.text((0,line),u"Curr RAM: %d kB" % (currentram),(192,192,192))
        line = line + lineheight
        self.draw.text((0,line),u"Diff RAM: %d kB" % (currentram-self.initialram),(192,192,192))
        line = line + lineheight
        self.draw.text((0,line),u"Lat: %.6f Lon %.6f" % (self.pos.lat, self.pos.lon),(192,192,192))
        line = line + lineheight
        #self.draw.text((0,line),u"Lines/Chars %d/%d" % (self.btr.linesread,self.btr.charsread),(192,192,192))
        self.draw.text((0,line),u"NMEA-lines read: %d" % (self.btr.linesread),(192,192,192))
        line = line + lineheight
        try:
            nmealine = self.pos.line
            nmeaname = nmealine[:6]
            self.draw.text((0,line),u"%s" % nmeaname,(192,192,192))
            line = line + lineheight
            nmealine = nmealine[6:]
            for i in range(1,len(nmealine),25):
                nmealinestart = nmealine[i:i+25]
                self.draw.text((0,line),u"%s" % nmealinestart,(192,192,192))
                line = line + lineheight
        except:
            pass
        self.draw_cellid()
        self.draw_ram()

    def draw_position(self):
        line = 14
        lineheight = 14
        #self.draw.text((0,line),u"Latitude:  %s°" % (self.pos.lat),(192,192,192),font=u'LatinBold19')
        # DO NOT define font! (pys60 1.2 Memory leak)
        self.draw.text((0,line),u"POSITION:",(192,192,192))
        line = line + lineheight
        self.draw.text((0,line),u"WGS84 Lat: %.6f°" % (self.pos.lat),(192,192,192))
        line = line + lineheight
        self.draw.text((0,line),u"WGS84 Lon: %.6f°" % (self.pos.lon),(192,192,192))
        line = line + lineheight
        speed = u"%.1f" % self.pos.speed_kmph
        self.draw.text((0,line),u"Speed: %s km/h" % (speed),(192,192,192))
        line = line + lineheight
        course = int(self.pos.course)
        self.draw.text((0,line),u"Course: %s°" % (course),(192,192,192))
        line = line + lineheight
        timestamp = time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(self.pos.getGpsUtcTime()))
        self.draw.text((0,line),u"UTC: %s" % (timestamp),(192,192,192))
        line = line + lineheight
        k=KKJWGS84()
        test = {}
        test['La'] = float(self.pos.lat)
        test['Lo'] = float(self.pos.lon)
        try:
            kkj = k.WGS84lalo_to_KKJxy(test)
            kkjp = int(kkj['P'])
            kkji = int(kkj['I'])
            self.draw.text((0,line),u"KKJ: P:%d I:%d" % (kkjp,kkji),(192,192,192))
        except:
            pass
        self.draw_cellid()
        self.draw_ram()
        #self.draw.rectangle((0,0,176,16),fill=(0,0,0))

    def draw_distance(self):
        """For temporary use, to be removed."""
        line = 14
        lineheight = 14
        timestamp = time.strftime("%H:%M:%S", time.localtime(self.pos.getGpsUtcTime()))
        self.draw.text((0,line),u"POI %s %d°" % (timestamp, self.pos.course),(192,192,192))
        line = line + lineheight
        if self.next_sortaction_time < time.time():
            self.sort_by_distance()
            # Schedule sorting POI-list next time after n secs
            self.next_sortaction_time = time.time() + self.next_sortaction_delay
        for i in range(0, len(self.pois)):
            if i > 15: break
            name = self.pois[i][2]
            d = self.pois[i][0] = self.calc.distance(self.pos.lat,self.pos.lon,self.pois[i][3],self.pois[i][4]) / 1000
            b = self.pois[i][1] = self.calc.bearing(self.pos.lat,self.pos.lon,self.pois[i][3],self.pois[i][4])
            #d = self.pois[i][0]
            #b = self.pois[i][1]
            self.draw.text((0,line),u"%.2f km %d° %s" % (d,b,name),(192,192,192))
            line = line + lineheight

    def sort_by_distance(self):
        for i in range(0, len(self.pois)):
            d = self.calc.distance(self.pos.lat,self.pos.lon,self.pois[i][3],self.pois[i][4]) / 1000
            b = self.calc.bearing(self.pos.lat,self.pos.lon,self.pois[i][3],self.pois[i][4])
            self.pois[i][0] = d
            self.pois[i][1] = b
        # print self.pois
        self.pois.sort()

    def speed_increase(self, kmph = 10):
        if self.speedlimit < 120:
            self.speedlimit = self.speedlimit + kmph
    def speed_decrease(self, kmph = 10):
        if self.speedlimit > 0:
            self.speedlimit = self.speedlimit - kmph
        
    def draw_speed(self):
        """For temporary use, to be removed."""
        self.canvas.bind(EKeyUpArrow,lambda:self.speed_increase())
        self.canvas.bind(EKeyDownArrow,lambda:self.speed_decrease())
        f = u'LatinBold19'
        line = 30
        lineheight = 30
        speed = self.pos.speed_kmph # * 10
        if speed <= self.speedlimit: speedcolor = (0,255,0)
        elif speed <= self.speedlimit + 10: speedcolor = (255,255,0)
        else: speedcolor = (255,0,0)
        self.draw.clear(speedcolor)
        self.draw.text((0,line),u"SPEED:",(0,0,0),font=f)
        line = line + lineheight
        self.draw.text((30,line),u"Current: %d km/h" % (speed),(0,0,0),font=f)
        line = line + lineheight
        self.draw.text((30,line),u"Limit: %d km/h" % (self.speedlimit),(0,0,0),font=f)
        line = line + lineheight
        
    def draw_cellid(self):
        (mcc, mnc, lac, cellid) = location.gsm_location()
        gsm_cell = "%s/%s/%s/%s" % (mcc, mnc, lac, cellid)
        self.draw.text((0,168),u"GSM-cell: %s" % (gsm_cell),(192,192,192))

    def draw_ram(self):
        currentram = int(sysinfo.free_ram())/1024
        self.draw.text((0,182),u"RAM: %d-%d=%d kB" % (self.initialram,currentram,currentram-self.initialram),(192,192,192))

    def ask_exit(self):
        if appuifw.query(u'Confirm quit?', 'query') is True:
            self.app_running = 0
        else:
            self.app_running = 1
        
    def run(self):
        appuifw.app.exit_key_handler = self.ask_exit
        #appuifw.app.menu = [(u'Connect to GPS',self.start_gps),(u'Software version',self.about)]
        appuifw.app.menu = [(u'Connect to GPS',self.start_gps),\
                            (u'Disconnect from GPS',self.stop_gps),\
                            (u'Fetch POIs from net',self.fetch_pois_from_gpswaypointsnet),\
                            (u'Read POIs from file',self.read_pois),\
                            (u'Software version',self.about)]

        self.initialram = int(sysinfo.free_ram())/1024
        while self.app_running:
            if self.read_gps_running:
                try:
                    status, NMEAline = self.btr.readline()
                    self.pos.line = NMEAline
                    if NMEAline is not None and NMEAline is not "":
                        self.parser.parse_line(NMEAline)
                except:
                    self.btr.disconnect()
            self.redraw(())
            e32.ao_sleep(0.05)
            #e32.ao_sleep(self.screen_update_delay)
        self.close_canvas()
        self.btr.disconnect()
        
    def version(self):
        version = u"Pys60gps\n%s\nRevision:%s" % (self.lastchangeddate, self.revision)
        return version
        
    def about(self):
        appuifw.note(self.version(), 'info')

    def start_gps(self):
        """Start reading bluetooth gps in separate thread"""
        if self.read_gps_running:
            appuifw.note(u"Are we already connected?", 'info')
            return
        self.read_gps_running = True
        status, msg = self.btr.connect()
        thread.start_new_thread(self.save_logs,()) # Start saving logs to a file
        return
        #thread.start_new_thread(self.read_gps,()) # Start reading gpsbtgpsreader

    def stop_gps(self):
        """Start reading bluetooth gps in separate thread"""
        self.btr.disconnect()
        self.read_gps_running = False
        return


    def start_fetch_pois(self):
        """Start reading bluetooth gps in separate thread"""
        if self.fetch_pois_running:
            appuifw.note(u"Are we already fetching pois?", 'info')
            return
        thread.start_new_thread(self.fetch_pois_from_gpswaypointsnet,()) # Start reading gpsbtgpsreader
        
if __name__ == "__main__":        
    appuifw.app.screen='large'
    gpsapp = pys60gps()
    gpsapp.app_running = 1
    gpsapp.run()
    e32.ao_sleep(1.0)
    
