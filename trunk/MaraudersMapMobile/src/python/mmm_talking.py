from appuifw import *
from e32 import *

import mmm_mapui

def doNothing():
    note(u"Sorry can't do that!")

def loadMap():
    mmm_mapui.init()
    mmm_mapui.app_lock.wait()
    init()
    
def quit():
    app_lock.signal()

def init():
    app.body = canvas
    app.exit_key_handler = quit
    app.title = u"PhotoEditor"
    app.menu = options

canvas = Canvas()
title = u"Talking"
options = [
        (u"Mute", doNothing),
        (u"Loud Speaker", doNothing),
        (u"Hold", doNothing),
        (u"Share Location", loadMap)]
app_lock = Ao_lock()

if __name__ == "__main__":
    init()
    app_lock.wait()