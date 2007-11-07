from appuifw import *
from e32 import *

from mmm_map import *
import mmm_util

def doNothing():
    note(u"Sorry can't do that!")

def quit():
    app_lock.signal()

def main():
    mmm_util.saveAppState()
    print "mmm_mapui"
    app.body = canvas
    app.exit_key_handler = quit
    app.title = u"Map UI"
    app.menu = options
    app_lock.wait()
    
    #canvas.blit(map.image)
    #iconsMod.drawIcons(canvas, targetLoc)
    mmm_util.restoreAppState()

# UI elements
canvas = Canvas()
title = u"Map UI"
options = [
    (u"Zoom in (*)", doNothing),
    (u"Zoom out (#)", doNothing),
    (u"Satellite info", doNothing)]
app_lock = Ao_lock()

# Map elements
map = Map()
#userLoc = userLocMod.UserLoc(1005, 1075, 90)
#targetLoc = targetLocMod.TargetLoc(130, 200)

if __name__ == "__main__":
    main()