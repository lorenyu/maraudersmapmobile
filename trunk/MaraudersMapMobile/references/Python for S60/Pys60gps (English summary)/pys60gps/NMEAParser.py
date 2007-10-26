# -*- coding: iso-8859-15 -*-
# $Id: NMEAParser.py 244 2006-02-05 20:36:41Z arista $
# Copyright Aapo Rista 2005-2006

#FIXME: Change parser so it returns dictionary of values instead of updating position object

class NMEAParser:
    """NMEAParser gets one NMEAString as a parameter and
       returns currently nothing but updates the Position-object.
       In the future NMEAParser will return a dictionary of parsed values.
       Currentry there are functions for 
       '$GPRMC',  '$GPGGA', '$GPGSA', '$GPGSV', '$GPGLL' and '$GPVTG'
       NMEA-senteces."""

    id = u'$Id: NMEAParser.py 244 2006-02-05 20:36:41Z arista $' # DO NOT modify Id-string
    pos = None
    sat_state = {} # Last parsed state of satellites {'sat_id' : [Elevation, Azimuth, SignalNoiseRatio]}
    sat_state_temp = {} # State currently being parsed
    
    def __init__(self, pos): # To be removed
        try: # Parse revision and last change date
            ida = self.id.split(" ")
            self.revision = ida[2]
            self.lastchangeddate = ida[3]
        except:
            self.revision = u'undefined'
            self.lastchangeddate = u'undefined'
        self.pos = pos
        sentences_to_parse = {'GPRMC':1,  
                              'GPGGA':0, 
                              'GPGSA':0, 
                              'GPGSV':0, 
                              'GPGLL':0, 
                              'GPVTG':0}
        #senteces2parse = ('$GPRMC')
        
    def checksum(self, nmealine):
        """Calculate checksum of given NMEA-sentence"""
        # Reject nmealines shorter than 5 bytes or having not '*'
        if len(nmealine) < 5 or nmealine[-4] != '*': 
            return None 
        nmeastr = nmealine[1:-4]
        chksumstr = line[-3:].rstrip()
        chksum = 0
        for i in range(0, len(nmeastr)):
            chksum ^= ord(nmeastr[i:i+1])
        # FIXME: return true or false
        if checksumstr == ("%02X" % chksum):
            #print 'OK "%s" = "%02X"' % (chkstr, chksum)
            return True
        else:
            #print 'FAIL LINE %d: "%s" != "%02X"' % (i, checksumstr, chksum)
            return False
            
    def _parseNMEALatLon(self, lat, l1, lon, l2):
        """Parse location from NMEA sentence. (6027.1954,N,02512.2171,E)"""
        try:
            # Convert lat/lon string to float
            latitude = float(lat[0:2]) + (float(lat[2:4] + "." + lat[5:9])/60)
            longitude = float(lon[0:3]) + (float(lon[3:5] + "." + lon[6:10])/60)
            if l1 is "S":
                latitude = -latitude
            if l2 is "W":
                longitude = -longitude
            #latitude = float("%.6f" % latitude)
            #longitude = float("%.6f" % longitude)
            return latitude, longitude
        except:
            return (None, None)

    def parseGPRMC(self, NMEAline):
        """Parse GPRMC Sentence (Position and time)"""
        # $GPRMC,195640.000,A,6027.1954,N,02512.2171,E,7.57,255.79,290505,,*0C
        # $GPRMC,195641.000,A,6027.1948,N,02512.2129,E,7.31,254.13,290505,,*00
        # $GPRMC,195642.000,A,6027.1941,N,02512.2088,E,7.32,253.44,290505,,*06
        # FIXME: is this NMEA 2.3 compatible?
        if (NMEAline.count(",") == 11): # Expect 11 ','-delimiters (NMEA 2.2)
            (GPRMC,hhmmssss,status,lat,l1,lon,l2,speed_knots,course,ddmmyy,mvd,mdr_cs)=NMEAline.split(",")
        elif (NMEAline.count(",") == 12): # Expect 12 ','-delimiters (NMEA 2.3)
            (GPRMC,hhmmssss,status,lat,l1,lon,l2,speed_knots,course,ddmmyy,mvd,mdr,fix_cs)=NMEAline.split(",")
        else:
            print "Invalid GPRMC";
            return
        self.pos.gpsstatus = status
        self.pos.set_time(hhmmssss)
        self.pos.set_date(ddmmyy)
        self.pos.set_speed_knots(speed_knots)
        self.pos.set_course(course)
        if (status is 'A' and lat is not "" and lon is not ""):
            latitude, longitude = self._parseNMEALatLon(lat, l1, lon, l2)
            self.pos.set_lat_lon(latitude, longitude)
        
    def parseGPGGA(self, NMEAline):
        """Parse GPGGA Sentence (Fix data)"""
        # $GPGGA,195640.000,6027.1954,N,02512.2171,E,1,09,0.9,34.9,M,,,,0000*3C
        # $GPGGA,195641.000,6027.1948,N,02512.2129,E,1,09,0.9,35.5,M,,,,0000*30
        # $GPGGA,195642.000,6027.1941,N,02512.2088,E,1,09,0.9,36.0,M,,,,0000*36
        # $GPGGA,093454.108,,,,,0,00,,,M,,,,0000*33
        if (NMEAline.count(",") == 14): # Expect 14 ','-delimiters
            (GPGGA,hhmmssss,lat,l1,lon,l2,q,xx,pp,ab,M,cd,M,xx,nnnn)=NMEAline.split(",")
            self.pos.set_time(hhmmssss)
            #if (hhmmssss is not ""):
            #    self.pos.time = hhmmssss
            if (lat is not "" and lon is not ""):
                latitude, longitude = self._parseNMEALatLon(lat, l1, lon, l2)
                self.pos.set_lat_lon(latitude, longitude)
        else:
            print "Invalid GPGGA";

    def parseGPGSA(self, NMEAline):
        """Parse GPGSA Sentence (Active satellites)."""
        # $GPGSA,A,3,09,18,22,29,11,28,07,26,05,,,,2.1,0.9,1.9*37
        # $GPGSA,A,3,09,18,22,29,11,28,07,26,05,,,,2.1,0.9,1.9*37
        # $GPGSA,A,3,09,18,22,29,11,28,07,26,05,,,,2.1,0.9,1.9*37
        if (NMEAline.count(",") == 17): # Expect 17 ','-delimiters
            (GPGSA,m1,m2,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,PDOP,HDOP,VDOPcs) = NMEAline.split(",")
            VDOP,cs = VDOPcs.split("*")
            self.pos.PDOP = PDOP
            self.pos.HDOP = HDOP
            self.pos.VDOP = VDOP

    def parseGPGSV(self, NMEAline):
        """Parse GPGSV Sentence (Satellites in view)."""
        # $GPGSV,3,1,09,09,47,278,32,07,47,122,39,26,43,196,31,28,39,072,32*70
        # $GPGSV,3,2,09,29,32,186,34,18,21,282,32,22,21,316,32,11,15,039,23*79
        # $GPGSV,3,3,09,05,11,239,31*4F
        #FIXME: nothing resets self.pos.sat_fix if fix is lost
        if (NMEAline.count(",") >= 5):
            # Remove checksum from the end of the line
            NMEAline,cs = NMEAline.split("*")
            tokens = NMEAline.split(",")
            (GPRSV,seqcnt,seqnum,satellites) = tokens[:4]
            self.pos.satellites = satellites
            endline = NMEAline.split(",")[4:]
            # Evaluate all satellites from endline
            while len(endline) > 0:
                satid = endline.pop(0)
                elevation = endline.pop(0)
                azimuth = endline.pop(0)
                snratio = endline.pop(0)
                self.sat_state_temp[satid] = [elevation, azimuth, snratio]
            if seqcnt == seqnum:
                self.sat_state = {}
                self.sat_state = self.sat_state_temp
                self.sat_state_temp = {}
                sv = 0 # count satellites with fix
                for satid in self.sat_state.keys():
                    if self.sat_state[satid][2] is not '': sv = sv + 1
                    self.pos.sat_fix = sv

    def parseGPGLL(self, NMEAline):
        """Parse GPGLL Sentence (Position)."""
        # $GPGLL,6027.1956,N,02512.3605,E,215948.000,A*30
        # $GPGLL,6027.1957,N,02512.3606,E,215949.000,A*33
        # $GPGLL,6027.1958,N,02512.3608,E,215950.000,A*3A
        # FIXME: check NMEA 2.3 compatibility
        if (NMEAline.count(",") == 6): # Expect 6 ','-delimiters
            (GPGGA,lat,l1,lon,l2,hhmmssss,status_cs)=NMEAline.split(",")
            (status, cs) = status_cs.split("*")
            self.pos.gpsstatus = status
            self.pos.set_time(hhmmssss)
            if (status is 'A' and lat is not "" and lon is not ""):
                latitude, longitude = self._parseNMEALatLon(lat, l1, lon, l2)
                self.pos.set_lat_lon(latitude, longitude)

    def parseGPVTG(self, NMEAline):
        """Parse GPVTG Sentence (Course over ground)."""
        # $GPVTG,213.81,T,,M,1.19,N,2.2,K*60
        # $GPVTG,78.97,T,,M,0.72,N,1.3,K*56
        # $GPVTG,66.09,T,,M,1.50,N,2.8,K*57
        # FIXME: check NMEA 2.3 compatibility
        if (NMEAline.count(",") == 8): # Expect 8 ','-delimiters (NMEA 2.2)
            (GPVTG,course_true,T,course_magn,M,speed_knots,N,speed_kmph,K_cs)=NMEAline.split(",")
        elif (NMEAline.count(",") == 9): # Expect 8 ','-delimiters (NMEA 2.3)
            (GPVTG,course_true,T,course_magn,M,speed_knots,N,speed_kmph,K,fix_cs)=NMEAline.split(",")
            #(K, cs) = K_cs.split("*") # unnecessary
            self.pos.set_speed_kmph(speed_kmph)
            self.pos.set_course(course_true)

    #To be changed to general parser
    def parse_line(self, NMEAline):
        NMEAname = NMEAline[0:6]
        if (NMEAname == "$GPRMC"):
            self.parseGPRMC(NMEAline)
        #elif (NMEAname == "$GPGGA"):
        #    self.parseGPGGA(NMEAline)
        elif (NMEAname == "$GPGSA"):
            self.parseGPGSA(NMEAline)
        #elif (NMEAname == "$GPGSV"):
        #    self.parseGPGSV(NMEAline)
        #elif (NMEAname == "$GPGLL"):
        #    self.parseGPGLL(NMEAline)
        #elif (NMEAname == "$GPVTG"):
        #    self.parseGPVTG(NMEAline)
