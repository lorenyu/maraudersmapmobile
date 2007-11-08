from appuifw import *
from e32 import *
from graphics import *
from mmm_map import *
from key_codes import *

import positioning

# Map elements

userX = -122.170715
userY = 37.424196
panX = 0
panY = 0

gpsX_per_pixel = 0.00000537
gpsY_per_pixel = -0.00000427

pixels_per_gpsX = 186220
pixels_per_gpsY = -234192


#userLoc = userLocMod.UserLoc(1005, 1075, 90)
#targetLoc = targetLocMod.TargetLoc(130, 200)

def doNothing():
    print "Do nothing"

def map_quit():
    positioning.stop_position()
    map_lock.signal()

def loading_quit():
    global loadCancelled
    loadCancelled = True
    app.screen = 'normal'
    app.body = canvas
    app.exit_key_handler = quit
    app.title = title
    app.menu = options
    
def loadMap():
    print "mmm_mapui"
    global loadCancelled
    app.screen = 'large'
    app.body = loading_canvas
    loading_canvas.clear((255, 255, 255))
    loading_canvas.blit(loading_image)
    app.menu = loading_options
    app.exit_key_handler = loading_quit
    loadCancelled = False
    
    ao_sleep(1)
    if not loadCancelled:
        app.screen = 'full'
        app.exit_key_handler = map_quit
        app.body = map_canvas
        app.title = map_title
        app.menu = map_options
        map_canvas.clear((255,255,255))
        
        
        map_canvas.blit(map.image)
        map_canvas.blit(map.overlay, mask = map.overlay_mask)
                
        #iconsMod.drawIcons(canvas, targetLoc)
        
        map_lock.wait()
        app.screen = 'normal'
        app.body = canvas
        app.exit_key_handler = quit
        app.title = title
        app.menu = options
    
def loading_redraw(rect):
    loading_canvas.blit(loading_image)
    
def quit():
    app_lock.signal()

def map_redraw(rect):
    dx = (userX - map.coords['gpsXMin']) * pixels_per_gpsX
    dy = (userY - map.coords['gpsYMax']) * pixels_per_gpsY
    
    w, h = map_canvas.size
    map.x = w/2 - dx + panX
    map.y = h/2 - dy + panY
    
    map_canvas.blit(map.image, target = (map.x, map.y))
    map_canvas.blit(map.overlay, mask = map.overlay_mask)
    map_canvas.blit(user_icon, mask = user_icon_mask, target = (w/2 + panX, h/2 + panY))
        
def redraw(rect):
    canvas.blit(image)
    
def zoom_in():
    if map.zoom > 2.5:
        map.zoom = 2.5
        return
    w, h = map.orig_image.size
    map.zoom = map.zoom + 0.2
    map.image = map.orig_image.resize((map.zoom*w, map.zoom*h))
    map_redraw(None)

def zoom_out():
    if map.zoom < 0.3:
        map.zoom = 0.2
        return
    w, h = map.orig_image.size    
    map.zoom = map.zoom - 0.2
    map.image = map.orig_image.resize((map.zoom*w, map.zoom*h))
    map_redraw(None)

def pan_up():
    global panY
    panY = panY + 10
    map_redraw(None)

def pan_down():
    global panY
    panY = panY- 10
    map_redraw(None)
    
def pan_left():
    global panX
    panX = panX + 10
    map_redraw(None)
    
def pan_right():
    global panX
    panX = panX - 10
    map_redraw(None)
    
# Map
map_canvas = Canvas(redraw_callback = map_redraw)
map_title = u"Map UI"
map_options = [
    (u"Zoom in (*)", doNothing),
    (u"Zoom out (#)", doNothing),
    (u"Satellite info", doNothing)]
map_lock = Ao_lock()    
map_canvas.bind(EKeyStar, zoom_in)
map_canvas.bind(EKeyHash, zoom_out)
map_canvas.bind(EKeyUpArrow, pan_up)
map_canvas.bind(EKeyDownArrow, pan_down)
map_canvas.bind(EKeyLeftArrow, pan_left)
map_canvas.bind(EKeyRightArrow, pan_right)
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

user_icon = Image.open("C:\\Data\\Images\\userIcon.jpg")
user_icon_mask = Image.new(user_icon.size, mode = 'L')
user_icon_mask.blit(Image.open("C:\\Data\\Images\\userIcon_mask.jpg"))


print "mmm_talking"
app.body = canvas
app.exit_key_handler = quit
app.title = u"Talking"
app.menu = options

print "Loading image talking1.jpg"
image = Image.open("C:\\Data\\Images\\talking1.jpg")
canvas.blit(image)

app_lock.wait()