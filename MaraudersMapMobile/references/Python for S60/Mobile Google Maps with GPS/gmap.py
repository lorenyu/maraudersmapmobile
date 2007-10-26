# gmap.py
#
# License : GPL
# http://www.gnu.org/copyleft/gpl.html
# (c) Rhys Jones 2005
# rhys.jones@calso.co.uk
#
# A demonstration Python application for Nokia phones that links a 
# Bluetooth GPS to retrieve and display Google Maps in realtime.
# It is very limited, and will only show 30 or so map tiles before
# giving a system error since too many Content_handlers are open.
# The next release of the Nokia Python sdk should allow better UI
# and graphics capabilities, such as:
#
# - overlaying current position on map tile
# - rotate and centre tiles to current GPS heading
# - background downloading of adjacent tiles
# - incorporate speed, position, satellites, etc. in UI
# 
# Thanks to:
# Google Map info:
# http://jgwebber.blogspot.com/2005/02/mapping-google.html
# Bluetooth and GPS info:
# http://www.postneo.com/postwiki/moin.cgi/PythonForSeries60


import appuifw
import urllib
import e32
import socket
import time

class App:
    def __init__(self):
        self.currentURL=None
        self.optionList = ({'start':u'Start'},{'exit':u'Exit'})
        self.lock = e32.Ao_lock()
        self.old_exit_key = appuifw.app.exit_key_handler
        appuifw.app.exit_key_handler = self.exit_handler
        self.current_tab = 0
        appuifw.app.set_tabs([u'Google Maps GPS'], self.display_tab)
        self.display_tab(0)
        self.lock.wait()

    def exit_handler(self):
        self.lock.signal()

    def display_tab(self, id):
        appuifw.app.body = appuifw.Listbox(self.optionList[id].values(), self.load)
        self.current_tab = id

    def load(self):
        haveFix=0
        latitude_in=0
        longitude_in=0
        
        self.sock=socket.socket(socket.AF_BT,socket.SOCK_STREAM)
        address,services=socket.bt_discover()
        target=(address,services.values()[0]) 
        self.sock.connect(target)

        while 1:
      buffer=""
      ch=self.sock.recv(1)
      while(ch!='$'):
        ch=self.sock.recv(1)
      while 1:
          if (ch=='\r'):
        break
          buffer+=ch
          ch=self.sock.recv(1)
      if (buffer[0:6]=="$GPGGA"):
          try:
        (GPGGA,utcTime,lat,ns,lon,ew,posfix,sats,hdop,alt,altunits,sep,sepunits,age,sid)=buffer.split(",")
        latitude_in=float(lat)
        longitude_in=float(lon)
        haveFix=int(posfix)
          except:
        haveFix=0

          if haveFix:
        zoom=2
        if ns == 'S':
            latitude_in = -latitude_in
        if ew == 'W':
            longitude_in = -longitude_in

        latitude_degrees = int(latitude_in/100)
        latitude_minutes = latitude_in - latitude_degrees*100

        longitude_degrees = int(longitude_in/100)
        longitude_minutes = longitude_in - longitude_degrees*100

        latitude = latitude_degrees + (latitude_minutes/60)
        longitude = longitude_degrees + (longitude_minutes/60)

        x=int(int((longitude + 98.35) * (131072 >> zoom) * 0.77162458338772) / 128);
        y=int(int((39.5 - latitude) * (131072 >> zoom)) / 128);

        url = "http://mt.google.com/mt?v=.1&x=%s&y=%s&zoom=%s"%(x, y, zoom)

        if url!=self.currentURL:
            try:
                id = appuifw.app.body.current()
                urllib.urlretrieve(url, "C:\\gmap.jpg")
                # Need to close previous image here...
                content_handler = appuifw.Content_handler()
                content_handler.open("C:\\gmap.jpg")
            except IOError:
                appuifw.note(u"Could not fetch the map.",'info')
            except Exception, E:
                appuifw.note(u"Could not open the map, %s"%E,'info')
            self.currentURL=url

      time.sleep(0.2)

A = App()