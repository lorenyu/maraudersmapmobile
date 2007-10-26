# -*- coding: iso-8859-15 -*-
# $Id: Track.py 240 2006-02-04 08:35:02Z arista $
# Copyright Aapo Rista 2005-2006

class Track:
    """Class Track holds resent trackpoints in the memory.
    If len(track) exceeds size, index start from zero again."""
    id = u'$Id: Track.py 240 2006-02-04 08:35:02Z arista $' # DO NOT modify Id-string

    def __init__(self, size = 10000):
        """Initialize Track-object with default size."""
        try: # Parse revision and last change date
            ida = self.id.split(" ")
            self.revision = ida[2]
            self.lastchangeddate = ida[3]
        except:
            self.revision = u'undefined'
            self.lastchangeddate = u'undefined'
        self.index = 0
        self.size = size
        self.track = []
        
    def push(self, trackrecord):
        """Push a trackpoint to the end of the track-list.
        The trackrecord is a list with values
        (lat, lon, alt, timestamputc)"""
        self.track.append(trackrecord)
        self.size = self.size + 1
        
    def __str__(self):
        """"""
        import time
        logstring = "# lat   \tlon\t        alt\ttime utc\n"
        for tp in self.track:
            (lat, lon, alt, timestamp) = tp
            timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timestamp))
            logstring = logstring + "%2.6f\t%2.6f\t%2.2f\t%s\n" % (lat, lon, alt, timestr)
        return logstring

if __name__ == "__main__":
    import random, time
    t = Track()
    time = (int)(time.time())
    for i in range(100):
        lat = float(random.random()+60)
        lon = float(random.random()+24.5)
        alt = float(random.random()*200)
        time = time + 5
        t.track.append([lat,lon,alt,time])
    print t
