# -*- coding: iso-8859-15 -*-
# $Id: KKJWGS84.py 240 2006-02-04 08:35:02Z arista $
###########################################################################
# Reference: news: <dmedg3$rck$1@phys-news4.kolumbus.fi>
# http://groups.google.fi/group/sfnet.keskustelu.paikannus/msg/5f2423756af7cccd
# 
# File:            KKJWGS84.py (Originally coordinates.py)
#
# Author:          Olli Lammi
#
# Version:         0.4a
#
# Date:            14.10.2005
#
# Functions:       KKJxy_to_WGS84lalo
#                  WGS84lalo_to_KKJxy
#                  KKJxy_to_KKJlalo
#                  KKJlalo_to_KKJxy
#                  KKJlalo_to_WGS84lalo
#                  WGS84lalo_to_KKJlalo
#                  KKJ_Zone_I
#                  KKJ_Zone_Lo
#                   
# Description:     Coordinate system functions. Initial code and alhorithms
#                  extracted from Viestikallio's PHP-source code 
#                  (http://www.viestikallio.fi/tools/kkj-wgs84.php). 
#                  Python translation and changes by Olli Lammi.
#
# Version history: ** 05.09.2005 v0.1a (Olli Lammi) **
#                  First version. Translated partially from PHP to Python.
#                  Original PHP code source: www.viestikallio.fi
# 
#                  ** 26.09.2005 v0.2a (Olli Lammi) **
#                  Included the WGS84_to_KKJxy -conversion.
#                  Changed all interfaces to work with degrees when
#                  using angle values
#                  Altered the KKJ zone info function to a
#                  lookup dictionary (self.KKJ_ZONE_INFO).
#                  Added function to calculate propable KKJ band
#                  from KKJ longitude (KKJ_Zone_Lo).
#                  
#                  ** 01.10.2005 v0.3a (Olli Lammi) **
#                  Small changes to function interfaces.
#
#                  ** 14.10.2005 v0.4a (Olli Lammi) **
#                  Added support for KKJ-bands 0 and 5.
#
###########################################################################
# Imports
import sys, os, string
import math
###########################################################################

class KKJWGS84:

    # Constants
    # Longitude0 and Center meridian of KKJ bands
    KKJ_ZONE_INFO = { 0: (18.0,  500000.0), \
                      1: (21.0, 1500000.0), \
                      2: (24.0, 2500000.0), \
                      3: (27.0, 3500000.0), \
                      4: (30.0, 4500000.0), \
                      5: (33.0, 5500000.0), \
                    }
    
    # Functions
    
    ###########################################################################
    # Function:  KKJxy_to_WGS84lalo
    ###########################################################################
    # Input:     dictionary with ['P'] is KKJ Northing
    #                            ['I'] in KKJ Eeasting
    # Output:    dictionary with ['La'] is latitude in degrees (WGS84)
    #                            ['Lo'] is longitude in degrees (WGS84)
    ###########################################################################
    def KKJxy_to_WGS84lalo(self, KKJin):  
      KKJz = self.KKJxy_to_KKJlalo(KKJin)
      WGS = self.KKJlalo_to_WGS84lalo(KKJz)
      return WGS
    
    ###########################################################################
    # Function:  WGS84lalo_to_KKJxy
    ###########################################################################
    # Input:     dictionary with ['La'] is latitude in degrees (WGS84)
    #                            ['Lo'] is longitude in degrees (WGS84)
    # Output:    dictionary with ['P'] is KKJ Northing
    #                            ['I'] in KKJ Eeasting
    ###########################################################################
    def WGS84lalo_to_KKJxy(self, WGSin):
      KKJlalo = self.WGS84lalo_to_KKJlalo(WGSin)
      ZoneNumber = self.KKJ_Zone_Lo(KKJlalo['Lo'])
      KKJxy = self.KKJlalo_to_KKJxy(KKJlalo, ZoneNumber)
      return KKJxy
    
    ###########################################################################
    # Function:  KKJlalo_to_WGS84lalo
    ###########################################################################
    def KKJlalo_to_WGS84lalo(self, KKJ):
      La = KKJ['La']
      Lo = KKJ['Lo']
      dLa = self.radians( 0.124867E+01      + \
                         -0.269982E+00 * La + \
                          0.191330E+00 * Lo + \
                          0.356119E-02 * La * La + \
                         -0.122312E-02 * La * Lo + \
                         -0.335514E-03 * Lo * Lo ) / 3600.0
      dLo = self.radians(-0.286111E+02      + \
                          0.114183E+01 * La + \
                         -0.581428E+00 * Lo + \
                         -0.152421E-01 * La * La + \
                          0.118177E-01 * La * Lo + \
                          0.826646E-03 * Lo * Lo ) / 3600.0
      WGS = {}
      WGS['La'] = self.degrees(self.radians(KKJ['La']) + dLa)
      WGS['Lo'] = self.degrees(self.radians(KKJ['Lo']) + dLo)
      return WGS
    
    ###########################################################################
    # Function:  WGS84lalo_to_KKJlalo
    ###########################################################################
    def WGS84lalo_to_KKJlalo(self, WGS):
      La = WGS['La']
      Lo = WGS['Lo']
      dLa = self.radians(-0.124766E+01      +           0.269941E+00 * La +                          -0.191342E+00 * Lo +  -0.356086E-02 * La * La +                          0.122353E-02 * La * Lo +                           0.335456E-03 * Lo * Lo ) / 3600.0
      dLo = self.radians( 0.286008E+02      + \
                         -0.114139E+01 * La + \
                          0.581329E+00 * Lo + \
                          0.152376E-01 * La * La + \
                         -0.118166E-01 * La * Lo + \
                         -0.826201E-03 * Lo * Lo ) / 3600.0
      KKJ = {}
      KKJ['La'] = self.degrees(self.radians(WGS['La']) + dLa)
      KKJ['Lo'] = self.degrees(self.radians(WGS['Lo']) + dLo)
      return KKJ
    
    ###########################################################################
    # Function:  KKJxy_to_KKJlalo
    ###########################################################################
    def KKJxy_to_KKJlalo(self, KKJ):  
      #
      # Scan iteratively the target area, until find matching
      # KKJ coordinate value.  Area is defined with Hayford Ellipsoid.
      #  
      LALO = {}
      ZoneNumber = self.KKJ_Zone_I(KKJ['I'])
      MinLa = self.radians(59.0)
      MaxLa = self.radians(70.5)
      MinLo = self.radians(18.5)
      MaxLo = self.radians(32.0)
      i = 1
      while (i < 35):
        DeltaLa = MaxLa - MinLa
        DeltaLo = MaxLo - MinLo
        LALO['La'] = self.degrees(MinLa + 0.5 * DeltaLa)
        LALO['Lo'] = self.degrees(MinLo + 0.5 * DeltaLo)
        KKJt = self.KKJlalo_to_KKJxy(LALO, ZoneNumber)
        if (KKJt['P'] < KKJ['P']):
          MinLa = MinLa + 0.45 * DeltaLa
        else:
          MaxLa = MinLa + 0.55 * DeltaLa
        if (KKJt['I'] < KKJ['I']):
          MinLo = MinLo + 0.45 * DeltaLo
        else:
          MaxLo = MinLo + 0.55 * DeltaLo
        i = i + 1
      return LALO
    
    ###########################################################################
    # Function:  KKJlalo_to_KKJxy
    ###########################################################################
    def KKJlalo_to_KKJxy(self, INP, ZoneNumber):
      Lo = self.radians(INP['Lo']) - self.radians(self.KKJ_ZONE_INFO[ZoneNumber][0])
      a  = 6378388.0            # Hayford ellipsoid
      f  = 1/297.0
      b  = (1.0 - f) * a
      bb = b * b              
      c  = (a / b) * a        
      ee = (a * a - bb) / bb  
      n = (a - b)/(a + b)     
      nn = n * n              
      cosLa = math.cos(self.radians(INP['La']))
      NN = ee * cosLa * cosLa 
      LaF = math.atan(math.tan(self.radians(INP['La'])) / math.cos(Lo * math.sqrt(1 + NN)))
      cosLaF = math.cos(LaF)
      t   = (math.tan(Lo) * cosLaF) / math.sqrt(1 + ee * cosLaF * cosLaF)
      A   = a / ( 1 + n )
      A1  = A * (1 + nn / 4 + nn * nn / 64)
      A2  = A * 1.5 * n * (1 - nn / 8)
      A3  = A * 0.9375 * nn * (1 - nn / 4)
      A4  = A * 35/48.0 * nn * n
      OUT = {}
      OUT['P'] = A1 * LaF - \
            A2 * math.sin(2 * LaF) + \
                A3 * math.sin(4 * LaF) - \
                    A4 * math.sin(6 * LaF)
      OUT['I'] = c * math.log(t + math.sqrt(1+t*t)) + \
            500000.0 + ZoneNumber * 1000000.0
      return OUT
    
    ###########################################################################
    # Function:  KKJ_Zone_I
    ###########################################################################
    def KKJ_Zone_I(self, KKJI):
      ZoneNumber = math.floor((KKJI/1000000.0))
      if ZoneNumber < 0 or ZoneNumber > 5:
          ZoneNumber = -1
      return ZoneNumber
    
    ###########################################################################
    # Function:  KKJ_Zone_Lo
    ###########################################################################
    def KKJ_Zone_Lo(self, KKJlo):
      # determine the zonenumber from KKJ easting
      # takes KKJ zone which has center meridian
      # longitude nearest (in math value) to
      # the given KKJ longitude
      ZoneNumber = 5
      while ZoneNumber >= 0:
        if math.fabs(KKJlo - self.KKJ_ZONE_INFO[ZoneNumber][0]) <= 1.5:
          break
        ZoneNumber = ZoneNumber - 1
      return ZoneNumber
    
    def degrees(self, rad):
        return rad * 180 / math.pi
    
    def radians(self, deg):
        return deg * math.pi / 180

if __name__ == "__main__":
    k=KKJWGS84()
    test = {}
    test['La'] = 60.00
    test['Lo'] = 25.00
    print k.WGS84lalo_to_KKJxy(test)
