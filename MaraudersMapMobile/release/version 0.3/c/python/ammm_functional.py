from appuifw import *
from e32 import *
from graphics import *
from mmm_map import *
from key_codes import *
from arrowLocMod import *
from math import sin, cos, pi, atan2

import positioning

# Map elements

#userGpsX = -122.170715
#userGpsY = 37.424196
userGpsX = -122.173156
userGpsY = 37.429900

targetGpsX = -122.173424
targetGpsY = 37.430778

allowShare = False  

def updatePosition(event):
    global userGpsX
    global userGpsY
    positionInfo = event['position']
    courseInfo = event['course']
    userGpsY = positionInfo['latitude']
    userGpsX = positionInfo['longitude']
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
arrowLoc = ArrowLoc(30, 30, 10)

def doNothing():
    print "Do nothing"

def loading_redraw(rect):
    if(app.body != loading_canvas):
        return
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
    app.body = loading_canvas
    app.screen = 'large'
    loading_canvas.clear((255, 255, 255))
    loading_canvas.blit(loading_image)
    loading_redraw(None)
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
        
        myMap.zoom = 1
        panX = 0
        panY = 0
        w, h = myMap.orig_image.size
        myMap.image = myMap.orig_image.resize((w, h))
        map_redraw(None)
                       
        map_lock.wait()
        app.screen = 'normal'
        app.body = canvas
        app.exit_key_handler = quit
        app.title = title
        app.menu = options
        redraw(None)

def map_redraw(rect):
    if(app.body != map_canvas):
        return
    
    dx = (userGpsX - myMap.coords['gpsXMin']) * (pixels_per_gpsX * myMap.zoom)
    dy = (userGpsY - myMap.coords['gpsYMax']) * (pixels_per_gpsY * myMap.zoom)
    
    targ_dx = (targetGpsX - userGpsX) * (pixels_per_gpsX * myMap.zoom)
    targ_dy = (targetGpsY - userGpsY) * (pixels_per_gpsY * myMap.zoom)
    
    w, h = map_canvas.size
    myMap.x = w/2 - dx + (panX * myMap.zoom)
    myMap.y = h/2 - dy + (panY * myMap.zoom)
    
    (iconW, iconH) = user_icon.size
    (targW, targH) = target_icon.size
    (targLabelW, targLabelH) = target_label.size
    
    userX = w/2 - iconW/2 + (panX * myMap.zoom)
    userY = h/2 - iconH/3 + (panY * myMap.zoom)
    
    targetX = w/2 + targ_dx + (panX * myMap.zoom)
    targetY = h/2 + targ_dy + (panY * myMap.zoom)
    
    map_canvas.blit(myMap.image, target = (myMap.x, myMap.y))    
    map_canvas.blit(user_icon, mask = user_icon_mask, target = (userX, userY))
    map_canvas.blit(target_icon, mask = target_icon_mask, target = (targetX - targW/2, targetY - targH/2))
    map_canvas.blit(target_label, mask = target_label_mask, target = (w/2 - targLabelW/2 +targ_dx + (panX * myMap.zoom), h/2 - targLabelH/2 + targ_dy + (panY * myMap.zoom) + 25)) 
    #map_canvas.blit(onebars_icon, mask = onebars_icon_mask, target = (184, 2))
    #map_canvas.blit(twobars_icon, mask = twobars_icon_mask, target = (184, 2))
    #map_canvas.blit(threebars_icon, mask = threebars_icon_mask, target = (184, 2))
    #map_canvas.blit(fourbars_icon, mask = fourbars_icon_mask, target = (184, 2))
    map_canvas.blit(fivebars_icon, mask = fivebars_icon_mask, target = (184, 2))
    map_canvas.blit(myMap.northIcon, mask = myMap.northIcon_mask, target = (w - myMap.northIcon.size[0] - 2, h - myMap.northIcon.size[1] - 30))
    map_canvas.blit(myMap.overlay, mask = myMap.overlay_mask)   
    
    
    if (not(targetX >= 0 and targetX < w and targetY >= 0 and targetY < h)):
        arrowLoc.theta = atan2(-(targetGpsY - userGpsY), targetGpsX - userGpsX)
        arrowLoc.draw(map_canvas)
        map_canvas.blit(target_label, mask = target_label_mask, target = (27 - 50/2, 58 + 2))

def map_quit():
    #positioning.stop_position()
    map_lock.signal()
    
def redraw(rect):
    if(app.body != canvas):
        return
    canvas.blit(image)

def quit():
    app.body = old_body
    app_lock.signal() 
    
# User manipulations   
def zoom_in():
    if myMap.zoom > 2.5:
        myMap.zoom = 2.5
        return
    w, h = myMap.orig_image.size
    newZoom = myMap.zoom + 0.2
    myMap.image = myMap.orig_image.resize((newZoom*w, newZoom*h))
    myMap.zoom = newZoom # only update zoom after image resizing is complete for consistency with other icons on the map
    map_redraw(None)

def zoom_out():
    if myMap.zoom < 0.3:
        myMap.zoom = 0.2
        return
    w, h = myMap.orig_image.size    
    newZoom = myMap.zoom - 0.2
    myMap.image = myMap.orig_image.resize((newZoom*w, newZoom*h))
    myMap.zoom = newZoom # only update zoom after image resizing is complete for consistency with other icons on the map
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
    #ao_sleep(20)
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
    if(app.body != prompting_canvas):
        return
    prompting_canvas.blit(prompting_image)
    
def prompting_quit():
    global allowShare
    allowShare = False
    prompting_lock.signal()
    loading_quit()
   
print "loading ICONS"
user_icon = Image.open("C:\\Data\\Images\\userIconCircle.jpg")
user_icon_mask = Image.new(user_icon.size, mode = 'L')
user_icon_mask.blit(Image.open("C:\\Data\\Images\\userIconCircle_mask.jpg"))

target_icon = Image.open("C:\\Data\\Images\\star1.jpg")
target_icon_mask = Image.new(target_icon.size, mode = 'L')
target_icon_mask.blit(Image.open("C:\\Data\\Images\\star_mask.jpg"))

target_label = Image.open("C:\\Data\\Images\\andyLabel.jpg")
target_label_mask = Image.new(target_label.size, mode = 'L')
target_label_mask.blit(Image.open("C:\\Data\\Images\\andyLabel_mask.jpg"))

#onebars_icon = Image.open("C:\\Data\\Images\\1bars.jpg")
#onebars_icon_mask = Image.new(onebars_icon.size, mode = 'L')
#onebars_icon_mask.blit(Image.open("C:\\Data\\Images\\1bars_mask.jpg"))

#twobars_icon = Image.open("C:\\Data\\Images\\2bars.jpg")
#twobars_icon_mask = Image.new(twobars_icon.size, mode = 'L')
#twobars_icon_mask.blit(Image.open("C:\\Data\\Images\\2bars_mask.jpg"))

#threebars_icon = Image.open("C:\\Data\\Images\\3bars.jpg")
#threebars_icon_mask = Image.new(threebars_icon.size, mode = 'L')
#threebars_icon_mask.blit(Image.open("C:\\Data\\Images\\3bars_mask.jpg"))

#fourbars_icon = Image.open("C:\\Data\\Images\\4bars.jpg")
#fourbars_icon_mask = Image.new(fourbars_icon.size, mode = 'L')
#fourbars_icon_mask.blit(Image.open("C:\\Data\\Images\\4bars_mask.jpg"))

fivebars_icon = Image.open("C:\\Data\\Images\\5bars.jpg")
fivebars_icon_mask = Image.new(fivebars_icon.size, mode = 'L')
fivebars_icon_mask.blit(Image.open("C:\\Data\\Images\\5bars_mask.jpg"))

# Prompting
prompting_image = Image.open("C:\\Data\\Images\\promptingToShare.jpg")
prompting_canvas = Canvas(redraw_callback = prompting_redraw)
prompting_canvas.blit(prompting_image)
prompting_canvas.bind(EKeyLeftSoftkey, temp)
prompting_options = [(u"Confirm", temp)]
prompting_lock = Ao_lock()

# Loading
loading_image = Image.open("C:\\Data\\Images\\loadingMap.jpg")
loading_canvas = Canvas(redraw_callback = loading_redraw)
loading_options = [
    (u"Mute", doNothing),
    (u"Loud Speaker", doNothing),
    (u"Hold", doNothing)]
loadingCancelled = False   
   
# Map
print "mymap stuff creating map ui"
myMap = Map()

map_canvas = Canvas(redraw_callback = map_redraw)
map_title = u"Map UI"
map_options = [
    (u"Zoom in (*)", zoom_in),
    (u"Zoom out (#)", zoom_out)]
    #(u"Satellite info", doNothing)]`
map_lock = Ao_lock()    
map_canvas.bind(EKeyStar, zoom_in)
map_canvas.bind(EKeyHash, zoom_out)
map_canvas.bind(EKeyUpArrow, pan_up)
map_canvas.bind(EKeyDownArrow, pan_down)
map_canvas.bind(EKeyLeftArrow, pan_left)
map_canvas.bind(EKeyRightArrow, pan_right)



# Talking
print "Loading image talking1.jpg"
#image = Image.open("C:\\Data\\Images\\talking1.jpg")
image = Image.new(Image.inspect("C:\\Data\\Images\\talking1.jpg")['size'])
image.load("C:\\Data\\Images\\talking1.jpg")
canvas = Canvas(redraw_callback = redraw)

title = u"Talking"
options = [
        (u"Mute", promptToShare),
        (u"Loud Speaker", doNothing),
        (u"Hold", doNothing),
        (u"Share Location", loadMap)]
app_lock = Ao_lock()


print "mmm_talking"
old_body = app.body
app.body = canvas
redraw(None)
app.exit_key_handler = quit
app.title = u"Talking"
app.menu = options



app_lock.wait()