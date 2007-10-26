# -*- coding: iso-8859-15 -*-
# $Id: BtGpsReader.py 241 2006-02-05 19:40:33Z arista $
# Copyright Aapo Rista 2005-2006

import socket, time, e32

if e32.in_emulator():
    # FIXME: GPS-simulation (used in emulator) must be implemented better!
    import random
    import Calculate

class BtGpsReader:
    """BtGpsReader - class to read lines of characters from Bluetooth GPS device."""
    id = u'$Id: BtGpsReader.py 241 2006-02-05 19:40:33Z arista $' # DO NOT modify Id-string
    linesread = 0
    charsread = 0
    connections = 0 # Total count of connection attempts
    discovers = 0   # Total count of discovers
    lastlineread = 0 # the timestamp of the latest successfully read line
    running = False
    target = None
    status = None
    sock = None
    file = None

    def __init__(self, target = None):
        """Initialize BtGpsReader. Set target if it was given"""
        try: # Parse revision and last change date
            ida = self.id.split(" ")
            self.revision = ida[2]
            self.lastchangeddate = ida[3]
        except:
            self.revision = u'undefined'
            self.lastchangeddate = u'undefined'
        self.status = "INITIALIZED"
        self.target = target
        if not e32.in_emulator():
            #self.sock = socket.socket(socket.AF_BT, socket.SOCK_STREAM)
            #self.file = self.sock.makefile(512) # create a buffered file object from the socket 
            pass
        else:
            self.speed = 0.0  # float km/h
            self.course = 0.0 # float 0.0 <= course < 360.0

    def discover(self):
        self.status = "DISCOVERING"
        self.discovers = self.discovers + 1
        # Return dummy bluetooth device if exeuted in emulator
        if e32.in_emulator():
            self.target=(u'du:mm:yb:lu:et:oo:th:de:vi:ce', 1)
            return "OK", "DISCOVERED"
        try:
            if self.sock is not None: # Release old socket
                self.sock = None
                self.file = None
            self.sock = socket.socket(socket.AF_BT, socket.SOCK_STREAM)
            self.file = self.sock.makefile(512) # create a buffered file object from the socket 
            address,services = socket.bt_discover()
            print "Discovered: %s, %s" % (address,services)
            self.target=(address, services.values()[0])
            return "OK", "DISCOVERED"
        except socket.error, why:
            print "ERROR in DISCOVER(), reason:"
            print why
            self.disconnect()
            self.status = "CONNECT_FAILED"
            return "ERROR", why

    def connect(self):
        """Connect to target. If target is None, use bt_discover to search bluetooth devices."""
        self.status = "CONNECTING"
        self.connections = self.connections + 1
        #print self.status
        # False connection if exeuted in emulator
        if e32.in_emulator():
            self.status = "CONNECTED"
            return "OK", "CONNECTED"
        try:
            self.linesread = 0
            if self.target is None:
                self.discover()
            if self.sock is not None: # Release old socket
                self.sock = None
                self.file = None
            self.sock=socket.socket(socket.AF_BT,socket.SOCK_STREAM)
            self.file = self.sock.makefile(512) # create a buffered file object from the socket 
            print "Connecting to "+str(self.target)
            self.sock.connect(self.target)
            self.status = "CONNECTED"
            return "OK", "CONNECTED"
        except socket.error, why:
            print "ERROR in connect(): %s" % (why)
            self.disconnect()
            self.status = "CONNECT_FAILED"
            return "ERROR", why

    def readline(self):
        """Read one line from Bluetooth GPS."""
        self.running = True
        if e32.in_emulator():
            e32.ao_sleep(0.5)
            return "OK", self.get_simulated_nmea_sentence()
        try:
           buffer = self.file.readline()
           self.linesread += 1
           self.lastlineread = time.clock()
           return "OK", buffer.strip()
        except socket.error, why:
            print "Socket.error:"
            print why
            self.status = "BROKEN_PIPE" # Check this
            print self.status
            self.disconnect()
            #return "ERROR", "GPS unreachable"
            return "ERROR", why

    def disconnect(self):
        self.status = "DISCONNECTED"
        print "Disconnecting..."
        if self.sock is not None:
            self.sock.close()
            self.sock = None
            self.file = None
        print "Disconnected."

    def get_age_of_last_line(self):
        return self.getAgeOfLastLine()

    def getAgeOfLastLine(self):
        """Return the age of last successfully read NMEA line in seconds."""
        if self.lastlineread > 0:
            return time.clock() - self.lastlineread
        elif self.lastlineread < 0:
           # Note: some S60 phones (etc. Nokia 6600, 3230) have broken time.clock():
           # it returns negative value around -1200000.0
            return -(self.lastlineread - time.clock())
        else: 
            return 0

    def get_simulated_nmea_sentence(self):
        ts = time.strftime("%H%M%S")
        ds = time.strftime("%d%m%y")
        la = random.randint(1000,2000)
        lo = random.randint(2000,3000)
        sp = random.randint(500,999)/100
        co = random.randint(0,180)/100
        return '$GPRMC,%s.000,A,6027.%4d,N,02512.%4d,E,%.2f,%.2f,%s,,*0C' % (ts,la,lo,sp,co,ds)
        nmea = [] #This to init!
        nmea.append('$GPRMC,195640.000,A,6027.1954,N,02512.2171,E,7.57,255.79,290505,,*0C')
        nmea.append('$GPRMC,195640.000,A,6027.1954,N,02512.2171,E,7.57,255.79,290505,,*0C')
        nmea.append('$GPRMC,195641.000,A,6027.1948,N,02512.2129,E,7.31,254.13,290505,,*00')
        nmea.append('$GPRMC,195642.000,A,6027.1941,N,02512.2088,E,7.32,253.44,290505,,*06')
        nmea.append('$GPGGA,195640.000,6027.1954,N,02512.2171,E,1,09,0.9,34.9,M,,,,0000*3C')
        nmea.append('$GPGGA,195641.000,6027.1948,N,02512.2129,E,1,09,0.9,35.5,M,,,,0000*30')
        nmea.append('$GPGGA,195642.000,6027.1941,N,02512.2088,E,1,09,0.9,36.0,M,,,,0000*36')
        nmea.append('$GPGGA,093454.108,,,,,0,00,,,M,,,,0000*33')
        nmea.append('$GPGSA,A,3,09,18,22,29,11,28,07,26,05,,,,2.1,0.9,1.9*37')
        nmea.append('$GPGSA,A,3,09,18,22,29,11,28,07,26,05,,,,2.1,0.9,1.9*37')
        nmea.append('$GPGSA,A,3,09,18,22,29,11,28,07,26,05,,,,2.1,0.9,1.9*37')
        nmea.append('$GPGSV,3,1,09,09,47,278,32,07,47,122,39,26,43,196,31,28,39,072,32*70')
        nmea.append('$GPGSV,3,2,09,29,32,186,34,18,21,282,32,22,21,316,32,11,15,039,23*79')
        nmea.append('$GPGSV,3,3,09,05,11,239,31*4F')
        nmea.append('$GPGLL,6027.1956,N,02512.3605,E,215948.000,A*30')
        nmea.append('$GPGLL,6027.1957,N,02512.3606,E,215949.000,A*33')
        nmea.append('$GPGLL,6027.1958,N,02512.3608,E,215950.000,A*3A')
        nmea.append('$GPVTG,213.81,T,,M,1.19,N,2.2,K*60')
        nmea.append('$GPVTG,78.97,T,,M,0.72,N,1.3,K*56')
        nmea.append('$GPVTG,66.09,T,,M,1.50,N,2.8,K*57')
        return nmea[0]

def read_lines(bt, line_cnt = 50):
    """Test method"""
    bt.connect()
    while bt.status is "CONNECTED":
        readstatus, NMEAline = bt.readline()
        if readstatus == "OK":
            print(u"%02d:%s...") % (bt.linesread, NMEAline[:21])
        else:
            print "ERROR! %s" % NMEAline
        if bt.linesread >= line_cnt:
            bt.disconnect()
            print "Closed"

if __name__ == "__main__":
    import e32
    bt = BtGpsReader()
    print "Connect 1"
    read_lines(bt, 10)
    for i in range(2,4):
        print "Sleep 5"
        e32.ao_sleep(5)
        print "Connect %d" % i
        read_lines(bt, 10)
    print "Finished!"
