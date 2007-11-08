from appuifw import *
from e32 import *
from graphics import *
from mmm_map import *

# Map elements

#userLoc = userLocMod.UserLoc(1005, 1075, 90)
#targetLoc = targetLocMod.TargetLoc(130, 200)

def doNothing():
    print "Do nothing"

def map_quit():
    map_lock.signal()

def loading_quit():
    global loadCancelled
    loadCancelled = True
    app.body = canvas
    app.exit_key_handler = quit
    app.title = title
    app.menu = options
    
def loadMap():
    print "mmm_mapui"
    global loadCancelled
    
    app.body = loading_canvas
    loading_canvas.clear((255, 255, 255))
    loading_canvas.blit(loading_image)
    app.menu = loading_options
    app.exit_key_handler = loading_quit
    loadCancelled = False
    
    ao_sleep(3)
    if not loadCancelled:
        app.exit_key_handler = map_quit
        app.body = map_canvas
        app.title = map_title
        app.menu = map_options
        map_canvas.clear((255,255,255))
            
        map_canvas.blit(map.image)
        #iconsMod.drawIcons(canvas, targetLoc)
        
        map_lock.wait()
        
        app.body = canvas
        app.exit_key_handler = quit
        app.title = title
        app.menu = options
    
def loading_redraw(rect):
    loading_canvas.blit(loading_image)
    
def quit():
    app_lock.signal()

def map_redraw(rect):
    map_canvas.blit(map.image)
    
def redraw(rect):
    canvas.blit(image)

# Map
map_canvas = Canvas(redraw_callback = map_redraw)
map_title = u"Map UI"
map_options = [
    (u"Zoom in (*)", doNothing),
    (u"Zoom out (#)", doNothing),
    (u"Satellite info", doNothing)]
map_lock = Ao_lock()    
map = Map()

# Loading
loading_image = Image.open("C:\\Data\\Images\\loadingMap.jpg")
loading_canvas = Canvas(redraw_callback = loading_redraw)
loading_options = [
    (u"Mute", doNothing),
    (u"Loud Speaker", doNothing),
    (u"Hold", doNothing)]
loadingCancelled = False    

# Talking
canvas = Canvas(redraw_callback = redraw)
title = u"Talking"
options = [
        (u"Mute", doNothing),
        (u"Loud Speaker", doNothing),
        (u"Hold", doNothing),
        (u"Share Location", loadMap)]
app_lock = Ao_lock()
 
print "mmm_talking"
app.body = canvas
app.exit_key_handler = quit
app.title = u"Talking"
app.menu = options

print "Loading image talking1.jpg"
image = Image.open("C:\\Data\\Images\\talking1.jpg")
canvas.blit(image)

app_lock.wait()