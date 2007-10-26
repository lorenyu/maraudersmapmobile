# -*- coding: iso-8859-15 -*-
# $Id: Calculate.py 236 2006-02-03 10:53:06Z arista $
# Copyright Aapo Rista 2005-2006

import math

class Calculate:
    """Calculate-object offers functions to calculate distance and bearing 
    between two coordinates."""

    id = u'$Id: Calculate.py 236 2006-02-03 10:53:06Z arista $' # DO NOT modify Id-string
    # Obsolete stuff
    a = 6378206.4 # North/South radius
    b = 6356583.8 # East/West radius
    # END obsolete
    nauticalmile = 1852.0 # Nautical mile in meters
    
    def __init__(self):
        try: # Parse revision and last change date
            ida = self.id.split(" ")
            self.revision = ida[2]
            self.lastchangeddate = ida[3]
        except:
            self.revision = u'undefined'
            self.lastchangeddate = u'undefined'

    def rad2deg(self, rad):
        """Convert radians to degrees.
        Return float radians."""
        return rad * 180 / math.pi

    def deg2rad(self, deg):
        """Convert degrees to radians.
        Return float degrees"""
        return deg * math.pi / 180

    def distance(self, lat1, lon1, lat2, lon2):
        """Calculate dinstance between two lat/lon pairs.
        Return float distance in meters."""
        lat1 = self.deg2rad(lat1)
        lon1 = self.deg2rad(lon1)
        lat2 = self.deg2rad(lat2)
        lon2 = self.deg2rad(lon2)
        theta = lon1 - lon2
        dist = math.sin(lat1) * math.sin(lat2) \
             + math.cos(lat1) * math.cos(lat2) * math.cos(theta)
        dist = math.acos(dist)
        dist = self.rad2deg(dist)
        meters = dist * 60 * 1852
        return meters
    
    # http://mathforum.org/library/drmath/view/55417.html
    # tc1=mod(atan2(sin(lon2-lon1)*cos(lat2),
    #         cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(lon2-lon1)),
    #         2*pi)
    def bearing(self, lat1, lon1, lat2, lon2):
        """Calculate bearing from lat1/lon1 to lat2/lon2.
        Return float bearing angle (0 <= bearing < 360)."""
        lat1 = self.deg2rad(lat1)
        lon1 = self.deg2rad(lon1)
        lat2 = self.deg2rad(lat2)
        lon2 = self.deg2rad(lon2)
        bearingradians = math.atan2(math.asin(lon2 - lon1) * math.cos(lat2), \
                                    math.cos(lat1) * math.sin(lat2) \
                                  - math.sin(lat1) * math.cos(lat2) * math.cos(lon2 - lon1))
        bearingdegrees = self.rad2deg(bearingradians)
        if (bearingdegrees < 0):
            bearingdegrees = 360 + bearingdegrees
        return bearingdegrees

    # Obsolete
    def _eta(self, lat): # Helper for _radius
        """Reduced or Parametric Latitude."""
        # NOTE: sqrt(1-e^2) == b/a
        return math.atan(self.rad2deg(self.b / self.a * math.tan(self.deg2rad(lat))))

    def _radius(self, lat): # Helper for newlatlon
        eta = self._eta(lat)
        x = self.a * math.cos(self.deg2rad(eta))
        y = self.b * math.sin(self.deg2rad(eta))
        return math.sqrt(x * x + y * y)

    def old_newlatlon(self, lat, lon, dist, bear):
        # http://www.perlmonks.org/?node=252153
        """Calculate new latitude and longitude from
        lat, lon, distance (meters) and bearing (degrees, 0 <= bearing < 360).
        Return (newlat, newlon)."""
        
        # Convert to radians
        lat = self.deg2rad(lat)
        # We do not need lon in radians.
        bear = self.deg2rad(bear)
        # Equations (5-5) and (5-6) in "Map Projections--A Working Manual"+, Page 31
        cosbear = math.cos(bear)
        sinbear = math.sin(bear)
        sinlat = math.sin(lat)
        coslat = math.cos(lat)
        dist = dist / self._radius(lat)
        cosdist = math.cos(dist)
        sindist = math.sin(dist)

        y = sindist * sinbear
        x = coslat * cosdist - sinlat * sindist * cosbear
        if x == 0.0 and y == 0.0:
            at = 0.0
        else:
            at = math.atan2(y, x)
        lat = self.rad2deg(math.asin(sinlat * cosdist + coslat * sindist * cosbear))
        lon = lon + self.rad2deg(at)
        return (lat, lon)
    # END Obsolete

    def newlatlon(self, lat, lon, dist, bear):
        """Calculate new latitude and longitude from
        lat, lon, distance (meters) and bearing (degrees, 0 <= bearing < 360).
        Return (newlat, newlon)."""
        bearrad = self.deg2rad(bear)
        # Latitude difference in degrees
        latdiff = ((dist / self.nauticalmile) * math.cos(bearrad)) / 60
        # Mean latitude
        midlat = lat + (latdiff / 2.0)
        # Longitude difference in degrees
        londiff = (dist / self.nauticalmile * math.sin(bearrad) / math.cos(midlat)) / 60
        return (lat + latdiff, lon + londiff)
        
    def test(self):
        lat1 = 60.0
        lon1 = 25.0
        dist1 = 1852/4.0 # meters
        bear1 = 0
        print "%10s %10s %10s %10s %10s"  % ("error%", "dist1(m)", "bear1°", "dist2(m)", "bear2°")
        for i in range(0,15):
            (lat2, lon2) = self.newlatlon(lat1 ,lon1, dist1, bear1)
            dist2 = self.distance(lat1, lon1, lat2, lon2)
            bear2 = self.bearing(lat1, lon1, lat2, lon2)
            error = abs((1-dist2/dist1)*100)
            print "%10.4f %10.2f %10.2f %10.2f %10.2f"  % (error, dist1, bear1, dist2, bear2)
            dist1 = dist1 * 2
        for i in range(0,3):
            print "Please implement test-function better!"

if __name__ == "__main__":
    c = Calculate()
    c.test()
    