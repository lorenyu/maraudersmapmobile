from appuifw import *
from e32 import *
from graphics import *
from mmm_map import *
from key_codes import *

import positioning

# Map elements

#userX = -122.170715
#userY = 37.424196
userX = -122.173156
userY = 37.429900

targetX = -122.173424
targetY = 37.430778

allowShare = False  


def updatePosition(event):
    global userX
    global userY
    positionInfo = event['position']
    courseInfo = event['course']
    userY = positionInfo['latitude']
    userX = positionInfo['longitude']
    map_redraw(None)

if (not(in_emulator())):
    positioning.set_requestors([{
        "type" : "service",
        "format" : "application",
        "data"   : "test_app"}])
    positioning.position(course = 1, callback = updatePosition, interval = 500000)
    
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

def loading_redraw(rect):
    loading_canvas.blit(loading_image)
    
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
    global panX
    global panY
    app.screen = 'large'
    app.body = loading_canvas
    loading_canvas.clear((255, 255, 255))
    loading_canvas.blit(loading_image)
    app.menu = loading_options
    app.exit_key_handler = loading_quit
    loadCancelled = False
    
    ao_sleep(0.5)
    
    if not loadCancelled:
        app.screen = 'full'
        app.exit_key_handler = map_quit
        app.body = map_canvas
        app.title = map_title
        app.menu = map_options
        #map_canvas.clear((255,255,255))
        
        map.zoom = 1
        panX = 0
        panY = 0
        w, h = map.orig_image.size
        map.image = map.orig_image.resize((w, h))
        map_redraw(None)
                       
        map_lock.wait()
        app.screen = 'normal'
        app.body = canvas
        app.exit_key_handler = quit
        app.title = title
        app.menu = options

def map_redraw(rect):
    dx = (userX - map.coords['gpsXMin']) * (pixels_per_gpsX * map.zoom)
    dy = (userY - map.coords['gpsYMax']) * (pixels_per_gpsY * map.zoom)
    
    targ_dx = (targetX - userX) * (pixels_per_gpsX * map.zoom)
    targ_dy = (targetY - userY) * (pixels_per_gpsY * map.zoom)
    
    w, h = map_canvas.size
    map.x = w/2 - dx + (panX * map.zoom)
    map.y = h/2 - dy + (panY * map.zoom)
    
    iconW, iconH = user_icon.size
    targW, targH = target_icon.size
    
    map_canvas.blit(map.image, target = (map.x, map.y))    
    map_canvas.blit(user_icon, mask = user_icon_mask, target = (w/2 - iconW/2 + (panX * map.zoom), h/2 - iconH/3 + (panY * map.zoom)))
    map_canvas.blit(target_icon, mask = target_icon_mask, target = (w/2 - targW/2 +targ_dx + (panX * map.zoom), h/2 - targH/2 + targ_dy + (panY * map.zoom)))
    #map_canvas.blit(onebars_icon, mask = onebars_icon_mask, target = (184, 2))
    #map_canvas.blit(twobars_icon, mask = twobars_icon_mask, target = (184, 2))
    #map_canvas.blit(threebars_icon, mask = threebars_icon_mask, target = (184, 2))
    #map_canvas.blit(fourbars_icon, mask = fourbars_icon_mask, target = (184, 2))
    map_canvas.blit(fivebars_icon, mask = fivebars_icon_mask, target = (184, 2))
    map_canvas.blit(map.overlay, mask = map.overlay_mask)   

def map_quit():
    positioning.stop_position()
    map_lock.signal()
    
def redraw(rect):
    canvas.blit(image)

def quit():
    app_lock.signal() 
    
# User manipulations   
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
    
# instead of doing ao_sleep, the socket connection just has to call this fn    
def promptToShare():
    app.screen = 'full'
    app.body = prompting_canvas
    prompting_redraw(None)
    app.menu = prompting_options
    app.exit_key_handler = prompting_quit
    
    prompting_lock.wait()
    if allowShare:
        loadMap()
  
def temp():
    global allowShare
    allowShare = True
    prompting_lock.signal()
    
def prompting_redraw(rect):
    prompting_canvas.blit(prompting_image)
    
def prompting_quit():
    global allowShare
    allowShare = False
    prompting_lock.signal()
    loading_quit()
    
# Map
map_canvas = Canvas(redraw_callback = map_redraw)
map_title = u"Map UI"
map_options = [
    (u"Zoom in (*)", zoom_in),
    (u"Zoom out (#)", zoom_out)]
    #(u"Satellite info", doNothing)]
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

# Prompting
prompting_image = Image.open("C:\\Data\\Images\\promptingToShare.jpg")
prompting_canvas = Canvas(redraw_callback = prompting_redraw)
prompting_canvas.bind(EKeyLeftSoftkey, temp)
prompting_options = [(u"Temp", temp)]
prompting_lock = Ao_lock()

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

target_icon = Image.open("C:\\Data\\Images\\star1.jpg")
target_icon_mask = Image.new(target_icon.size, mode = 'L')
target_icon_mask.blit(Image.open("C:\\Data\\Images\\star_mask.jpg"))

onebars_icon = Image.open("C:\\Data\\Images\\1bars.jpg")
onebars_icon_mask = Image.new(onebars_icon.size, mode = 'L')
onebars_icon_mask.blit(Image.open("C:\\Data\\Images\\1bars_mask.jpg"))

twobars_icon = Image.open("C:\\Data\\Images\\2bars.jpg")
twobars_icon_mask = Image.new(twobars_icon.size, mode = 'L')
twobars_icon_mask.blit(Image.open("C:\\Data\\Images\\2bars_mask.jpg"))

threebars_icon = Image.open("C:\\Data\\Images\\3bars.jpg")
threebars_icon_mask = Image.new(threebars_icon.size, mode = 'L')
threebars_icon_mask.blit(Image.open("C:\\Data\\Images\\3bars_mask.jpg"))

fourbars_icon = Image.open("C:\\Data\\Images\\4bars.jpg")
fourbars_icon_mask = Image.new(fourbars_icon.size, mode = 'L')
fourbars_icon_mask.blit(Image.open("C:\\Data\\Images\\4bars_mask.jpg"))

fivebars_icon = Image.open("C:\\Data\\Images\\5bars.jpg")
fivebars_icon_mask = Image.new(fivebars_icon.size, mode = 'L')
fivebars_icon_mask.blit(Image.open("C:\\Data\\Images\\5bars_mask.jpg"))

print "mmm_talking"
app.body = canvas
app.exit_key_handler = quit
app.title = u"Talking"
app.menu = options

print "Loading image talking1.jpg"
image = Image.open("C:\\Data\\Images\\talking1.jpg")
canvas.blit(image)

ao_sleep(0.5)
promptToShare()
app_lock.wait()