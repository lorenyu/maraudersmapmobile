from appuifw import *
from e32 import *
from graphics import *

#import mmm_mapui
import mmm_util

def doNothing():
    note(u"Sorry can't do that!")

def loadMap():
    mmm_mapui.main()
    
def quit():
    app_lock.signal()

def main():
    mmm_util.saveAppState()
    print "mmm_talking"
    app.body = canvas
    app.exit_key_handler = quit
    app.title = u"Talking"
    app.menu = options
    
    try:
        print "Loading image talking1.jpg"
        image = Image.open("C:\\Data\\Images\\talking1.jpg")
        canvas.blit(image)
    except Exception, e:
        print e
        note(unicode(e))
    
    app_lock.wait()
    mmm_util.restoreAppState()

canvas = Canvas()
title = u"Talking"
options = [
        (u"Mute", doNothing),
        (u"Loud Speaker", doNothing),
        (u"Hold", doNothing),
        (u"Share Location", loadMap)]
app_lock = Ao_lock()

if __name__ == "__main__":
    main()