# -*- coding: iso-8859-15 -*-
# $Id: Position.py 240 2006-02-04 08:35:02Z arista $
# Copyright Aapo Rista 2005-2006

import e32, time, sys, os

class Position:
    """Position-object keeps the current (or last defined) lat/long, position, speed etc."""
    id = u'$Id: Position.py 240 2006-02-04 08:35:02Z arista $' # DO NOT modify Id-string
    age = -2000000000 # Big negative integer because of bug in some phones
    gpsstatus = "V"
    linesread = 0
    charsread = 0
    line = ""
    lat = 0.0 # float -90.00 < lat < 90.00
    lon = 0.0 # float -180.00 < lon < 180.00
    alt = 0.0 # in feet/meters?
    speed = 0.0 # Speed is saved internally in kilmeteres per hour
    speed_knots = 0.0 # Speed in knots
    speed_kmph = 0.0 # Speed in kilometers per hour
    course = 0.0 # 0.0 <= course < 360.0
    sat_fix = 0 # satellites with S/N != ''
    satellites = 0 # in view
    time = "000000" # HHMMSS.SS
    date = "010170" # ddmmyy
    mode = 0   # 1 = No fix, 2 = 2D, 3 = 3D
    PDOP = 0.0 # Position dilution of precision
    HDOP = 0.0 # Horizontal dilution of precision
    VDOP = 0.0 # Vertical dilution of precision
    # GSM-location
    cellid = 0
    # Function definitions

    def __init__(self):
        try: # Parse revision and last change date
            ida = self.id.split(" ")
            self.revision = ida[2]
            self.lastchangeddate = ida[3]
        except:
            self.revision = u'undefined'
            self.lastchangeddate = u'undefined'

    def set_lat_lon(self, lat, lon):
        """Set latitude and longitude. Update age."""
        # TODO: check validity of lat/lon  here
        try:
            self.lat = float(lat)
            self.lon = float(lon)
            self.age = time.clock()
        except:
            print "Invalid lat/lon %s/%s" % (lat, lon)
            pass

    def set_time(self, hhmmssss):
        if (len(hhmmssss) >= 6):
            self.time = hhmmssss

    def set_date(self, ddmmyy):
        if (len(ddmmyy) == 6):
            self.date = ddmmyy

    def set_speed_kmph(self, speed_kmph):
        """Set speed. Argument is float kilometers per hour"""
        try:
            self.speed_kmph = float(speed_kmph)
        except:
            self.speed_kmph = 0.0

    def set_speed_knots(self, speed_knots):
        """Set speed. Argument is float knots"""
        try:
            self.speed_knots = float(speed_knots)
        except:
            self.speed_knots = 0.0
        self.speed_kmph = self.speed_knots * 1.852

    def set_course(self, course):
        """Set course over ground. Argument is float between 0 <= course < 360"""
        try:
            course = float(course)
        except:
            course = -1 # TODO: would None-type be better choise?
        if 0 <= course < 360: self.course = course
        else: self.course = -1

    def get_age(self):
        """Return the age of the last position update in seconds. (S.SS)"""
        if self.age > 0:
            return time.clock() - self.age
        elif self.age < 0:
           # Note: some S60 phones (etc. Nokia 6600, 3230) have broken time.clock():
           # it returns negative value around -1200000.0
            return -(self.age - time.clock())
        else:
            return 0

    def getGpsUtcTime(self):
        d = self.date
        t = self.time
        (year, mon, day) = (int("20"+d[4:6]), int(d[2:4]), int(d[0:2]))
        (hour, min, sec) = (int(t[0:2]), int(t[2:4]), int(t[4:6]))
        try:
            timestamp = time.mktime((year, mon, day, hour, min, sec, 0, 0, 0))
            return timestamp
        except:
            pass
        return 0
        
    def __str__(self):
        return "Lat: %s\nLon: %s\nDate: %s\nTime: %s" % (self.lat, self.lon, self.date, self.time)
