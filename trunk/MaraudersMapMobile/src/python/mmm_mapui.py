# mmm_mapUI.py

from appuifw import *
from graphics import *
from e32 import *
from key_codes import *
from mmm_utils import *
from mmm_targetArrow import *
from mmm_icons import *
from math import sin, cos, pi, atan2
import positioning

PIXELS_PER_GPSX = 186220
PIXELS_PER_GPSY = -234192

GPSX_PER_PIXEL = 0.00000537
GPSY_PER_PIXEL= -0.00000427

# hardcode target's coords
# Gates parking lot
#targetGpsX = -122.173424
#targetGpsY = 37.430778
# Herrin field
targetGpsX = -122.172177
targetGpsY = 37.429811

# if GPS not working, hardcode user's coords
# Gates GPS coords
#userGpsX = -122.173156
#userGpsY = 37.429900
# AT&T Terrace
userGpsX = -122.173505
userGpsY = 37.430328
# Tressider 
#userGpsX = -122.170715
#userGpsY = 37.424196

def updatePosition(event):
    global userGpsX
    global userGpsY
    positionInfo = event['position']
    courseInfo = event['course']
    userGpsY = positionInfo['latitude']
    userGpsX = positionInfo['longitude']
    app.redraw(None)

class MapUI:
    def __init__(self):
        def zoom_in():
            self.setZoom(self.zoom + 0.25)

        def zoom_out():
            self.setZoom(self.zoom - 0.25)
        
        def recenter():
            self.panX = 0
            self.panY = 0
            app.redraw(None)
            
        def pan_up():
            self.panY = self.panY + 10
            app.redraw(None)

        def pan_down():
            self.panY = self.panY- 10
            app.redraw(None)
                    
        def pan_left():
            self.panX = self.panX + 10
            app.redraw(None)
                    
        def pan_right():
            self.panX = self.panX - 10
            app.redraw(None)
    
        try:
            self.menu = [(u"Zoom in (*)", zoom_in),
                         (u"Zoom out (#)", zoom_out),
                         (u"Recenter (Select button)", recenter)]
            self.keyBindings = {
                EKeyStar : zoom_in,
                EKeyHash : zoom_out,
                EKeyUpArrow : pan_up,
                EKeyDownArrow : pan_down,
                EKeyLeftArrow : pan_left,
                EKeyRightArrow : pan_right,
                EKeySelect : recenter}
                         
            print "Loading map image"
            self.image = Image.open("C:\\Data\\Images\\gates_zoom_1.00.jpg")
            self.orig_image = self.image
            
            self.zoom = 1
            self.panX = 0
            self.panY = 0
            self.x = 0
            self.y = 0
            
            self.overlay = Image.open("C:\\Data\\Images\\mapui1.jpg")
            self.overlay_mask = Image.new(self.overlay.size, mode = 'L')
            self.overlay_mask.blit(Image.open("C:\\Data\\Images\\mapui1_mask.jpg"))
            self.northIcon = Image.open("C:\\Data\\Images\\northIcon.jpg")
            self.northIcon_mask = Image.new(self.northIcon.size, mode = 'L')
            self.northIcon_mask.blit(Image.open("C:\\Data\\Images\\northIcon_mask.jpg"))
            self.targetArrow = TargetArrow(30, 30, 0)
            
            print "Loading map coords"
            f = file(u"C:\\Data\\Others\\gates_coords.txt", "r")
            str = ""
            for line in f:
                str += line.strip()
            f.close()
            mapCoords = eval(str)		
            self.coords = mapCoords
            
            self.lock = Ao_lock()
            print "Map coords: ", self.coords
        except Exception, e:
            print e
        
    def run(self):
        def quit():
            positioning.stop_position()
            self.lock.signal()
            
        def redraw(rect):
            self.draw()
            
        saveState()
        setKeyBindings(self.keyBindings)
        
        self.setZoom(1)
        self.panX = 0
        self.panY = 0
        if (not(in_emulator())):
            positioning.set_requestors([{
                "type" : "service",
                "format" : "application",
                "data"   : "test_app"}])
            positioning.position(course = 1, callback = updatePosition, interval = 500000)
        
        app.screen = 'full'
        app.menu = self.menu
        app.redraw = redraw
        app.redraw(None)
        app.exit_key_handler = quit
        self.lock.wait()
        restoreState()
    
    def setZoom(self, zoom):
        if (zoom < 0.75):
            zoom = 0.75
        if (zoom > 1.5):
            zoom = 1.5
        
        if (self.zoom == zoom):
            return
            
        (w, h) = self.orig_image.size
        #self.image = self.orig_image.resize((zoom*w, zoom*h))
        
        self.image = Image.open("C:\\Data\\Images\\gates_zoom_%.2f.jpg" % zoom)
        self.zoom = zoom # only update zoom after image resizing is complete for consistency with other icons on the map
        app.redraw(None)
        
    def draw(self):
        w, h = app.body.size
            
        # draw map
        dx = (userGpsX - self.coords['gpsXMin']) * (PIXELS_PER_GPSX * self.zoom)
        dy = (userGpsY - self.coords['gpsYMax']) * (PIXELS_PER_GPSY * self.zoom)
        self.x = w/2 - dx + (self.panX * self.zoom)
        self.y = h/2 - dy + (self.panY * self.zoom)
        app.body.blit(self.image, target = (self.x, self.y))
        
        # draw user
        userX = w/2 + (self.panX * self.zoom)
        userY = h/2 + (self.panY * self.zoom)
        (iconW, iconH) = userIcon.size
        app.body.blit(userIcon, mask = userIcon_mask, target = (userX - iconW/2, userY - iconH/3))
        
        # draw target
        targ_dx = (targetGpsX - userGpsX) * (PIXELS_PER_GPSX * self.zoom)
        targ_dy = (targetGpsY - userGpsY) * (PIXELS_PER_GPSY * self.zoom)
        targetX = w/2 + targ_dx + (self.panX * self.zoom)
        targetY = h/2 + targ_dy + (self.panY * self.zoom)
        (targW, targH) = targetIcon.size
        app.body.blit(
            targetIcon,
            mask = targetIcon_mask,
            target = (targetX - targW/2, targetY - targH/2))
        (targLabelW, targLabelH) = targetLabel.size
        app.body.blit(
            targetLabel,
            mask = targetLabel_mask,
            target = (targetX - targLabelW/2, targetY + targH/2))

        # draw signal strength               
        #app.body.blit(onebarsIcon, mask = onebarsIcon_mask, target = (184, 2))
        #app.body.blit(twobarsIcon, mask = twobarsIcon_mask, target = (184, 2))
        #app.body.blit(threebarsIcon, mask = threebarsIcon_mask, target = (184, 2))
        #app.body.blit(fourbarsIcon, mask = fourbarsIcon_mask, target = (184, 2))
        app.body.blit(fivebarsIcon, mask = fivebarsIcon_mask, target = (184, 2))
        
        # draw arrow indicating north
        app.body.blit(self.northIcon, mask = self.northIcon_mask, target = (w - self.northIcon.size[0] - 2, h - self.northIcon.size[1] - 30))
        
        # draw map ui controls
        app.body.blit(self.overlay, mask = self.overlay_mask)   
        
        # if target is offscreen, draw arrow indicating direction of target
        if (not(targetX >= 0 and targetX < w and targetY >= 0 and targetY < h)):
            self.targetArrow.theta = atan2(-(targetGpsY - userGpsY), targetGpsX - userGpsX)
            self.targetArrow.draw(app.body)
            (targetLabelW, targetLabelH) = targetLabel.size
            app.body.blit(targetLabel, mask = targetLabel_mask, target = (30 - targetLabelW/2, 30 + self.targetArrow.radius))
    
if __name__ == "__main__":
    map = MapUI()