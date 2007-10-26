# -*- coding: iso-8859-15 -*-
# $Id: Logger.py 240 2006-02-04 08:35:02Z arista $
# Copyright Aapo Rista 2005-2006

import time
class Logger:
    """"""
    id = u'$Id: Logger.py 240 2006-02-04 08:35:02Z arista $' # DO NOT modify Id-string

    def __init__(self, log_name):
        """"""
        try: # Parse revision and last change date
            ida = self.id.split(" ")
            self.revision = ida[2]
            self.lastchangeddate = ida[3]
        except:
            self.revision = u'undefined'
            self.lastchangeddate = u'undefined'
        self.logfile = log_name

    def write(self, obj):
        """"""
        log_file = open(self.logfile, 'a')
        timestamp = u"%s: " % (time.strftime("%Y%m%d-%H%M%S"))
        log_file.write(timestamp)
        log_file.write(obj)
        log_file.write(u"\n")
        log_file.close()

    def writelines(self, obj):
        """"""
        self.write(''.join(list))

    def flush(self):
        pass
