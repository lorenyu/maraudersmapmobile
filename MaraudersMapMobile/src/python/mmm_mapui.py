# mmm_mapUI.py

from appuifw import *
from graphics import *
from e32 import *
from key_codes import *
from mmm_utils import *
from mmm_targetArrow import *
from mmm_icons import *
from math import sin, cos, pi, atan2, pow, sqrt
import positioning
import mmm_color

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

def addOffset((x, y), (dx, dy) ):
    return (x + dx, y + dy)

def getPanArrowVertices():
    vertices = [(16, 0), (32, 14), (16, 8), (0, 14)]
    up = []
    down = []
    left = []
    right = []
    for i in range(0, 4):
        up.append( addOffset(vertices[i], (104, 5) ) )
        down.append( addOffset(rotate(vertices[i], pi), (136, 313) )) 
        left.append( addOffset(rotate(vertices[i], (-pi/2)), (5, 175)))
        right.append( addOffset(rotate(vertices[i], (pi/2)), (233, 144)))
    return up, down, left, right

def getArrow(color):
    arrow = TargetArrow(30, 30, 0)
    arrow.isCircleVisible = False
    arrow.setScale(0.5)
    arrow.color = color
    return arrow
    
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
            self.panY += 10
            h = app.body.size[1]
            dy = (userGpsY - self.coords['gpsYMax']) * (PIXELS_PER_GPSY * self.zoom)
            tempY = h/2 - dy + (self.panY * self.zoom)
            if (tempY >= 0):
                self.panY -= 10
                note(u"You have reached the end of the map.")
                return
            app.redraw(None)

        def pan_down():
            self.panY -= 10
            h = app.body.size[1]
            dy = (userGpsY - self.coords['gpsYMax']) * (PIXELS_PER_GPSY * self.zoom)
            tempY = h/2 - dy + (self.panY * self.zoom)
            tempY += self.image.size[1]
            if (tempY <= h):
                self.panY += 10
                note(u"You have reached the end of the map.")
                return
            app.redraw(None)
                    
        def pan_left():
            self.panX += 10
            w = app.body.size[0]
            dx = (userGpsX - self.coords['gpsXMin']) * (PIXELS_PER_GPSX * self.zoom)
            tempX = w/2 - dx + (self.panX * self.zoom)
            if (tempX >= 0):
                self.panX -= 10
                note(u"You have reached the end of the map.")
                return
            app.redraw(None)
                    
        def pan_right():
            self.panX -= 10
            w = app.body.size[0]
            dx = (userGpsX - self.coords['gpsXMin']) * (PIXELS_PER_GPSX * self.zoom)
            tempX = w/2 - dx + (self.panX * self.zoom)
            tempX += self.image.size[0]
            if (tempX <= w):
                self.panX += 10
                note(u"You have reached the end of the map.")
                return
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
                EKeySelect : recenter,
                EKey5 : takeScreenShot}
                         
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
            self.targetArrow = getArrow(mmm_color.GOLD)
            self.userArrow = getArrow(mmm_color.BLUE)
            self.upVertices, self.downVertices, self.leftVertices, self.rightVertices = getPanArrowVertices()
            
            print "Loading map coords"
            f = file(u"C:\\Data\\Others\\gates_coords.txt", "r")
            str = ""
            for line in f:
                str += line.strip()
            f.close()
            self.coords = eval(str)		
            
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
            note(u"You cannot zoom further.")
            zoom = 0.75
        if (zoom > 1.5):
            note(u"You cannot zoom further.")
            zoom = 1.5
        
        if (self.zoom == zoom):
            return
            
        #(w, h) = self.orig_image.size
        #self.image = self.orig_image.resize((zoom*w, zoom*h))
        
        self.image = Image.open("C:\\Data\\Images\\gates_zoom_%.2f.jpg" % zoom)
        self.zoom = zoom # only update zoom after image resizing is complete for consistency with other icons on the map
        w = app.body.size[0]
        dx = (userGpsX - self.coords['gpsXMin']) * (PIXELS_PER_GPSX * self.zoom)
        tempX = w/2 - dx + (self.panX * self.zoom)
        if (tempX >= 0):
            self.panX  = (dx - w/2) / self.zoom
        elif (tempX + self.image.size[0] < w): 
            self.panX = (w - self.image.size[0] + dx - w/2) / self.zoom
        h = app.body.size[1]
        dy = (userGpsY - self.coords['gpsYMax']) * (PIXELS_PER_GPSY * self.zoom)
        tempY = h/2 - dy + (self.panY * self.zoom)
        if (tempY > 0):
            self.panY = (dy - h/2) / self.zoom
        elif (tempY + self.image.size[1] < h): 
            self.panY = (h - self.image.size[1] + dy - h/2) / self.zoom
        app.redraw(None)
    
    def computeArrowLocation(self, (x1, y1), (x2, y2), arrowRadius):
        (x1, y1) = (float(x1), float(y1))
        (x2, y2) = (float(x2), float(y2))
        
        # compute Ax + By = 1
        det = x1 * y2 - x2 * y1
        if (det == 0):
            A = -y2 + y1
            B = x2 - x1
        else:
            A = (y2 - y1) / det
            B = (-x2 + x1) / det
        
        (w, h) = app.body.size
        # find intersections with sides
        if (x2 < x1):
            y = (1 - A*arrowRadius) / B
            if (y >= arrowRadius and y < h - arrowRadius):
                return (arrowRadius, y)
        if (x2 > x1):
            y = (1 - A*(w - arrowRadius)) / B
            if (y >= arrowRadius and y < h - arrowRadius):
                return (w - arrowRadius, y)
        if (y2 < y1):
            x = (1 - B*arrowRadius) / A
            if (x >= arrowRadius and x < w - arrowRadius):
                return (x, arrowRadius)
        if (y2 > y1):
            x = (1 - B*(h - arrowRadius)) / A
            if (x >= arrowRadius and x < w - arrowRadius):
                return (x, h - arrowRadius)
        return (0, 0)
        
    def draw(self):
        w, h = app.body.size
        
        # draw map
        dx = (userGpsX - self.coords['gpsXMin']) * (PIXELS_PER_GPSX * self.zoom)
        dy = (userGpsY - self.coords['gpsYMax']) * (PIXELS_PER_GPSY * self.zoom)
        self.x = w/2 - dx + (self.panX * self.zoom)
        self.y = h/2 - dy + (self.panY * self.zoom)
        app.body.blit(self.image, target = (self.x, self.y))
        
        # user and target coordinates, and target direction
        userX = w/2 + (self.panX * self.zoom)
        userY = h/2 + (self.panY * self.zoom)
        targ_dx = (targetGpsX - userGpsX) * (PIXELS_PER_GPSX * self.zoom)
        targ_dy = (targetGpsY - userGpsY) * (PIXELS_PER_GPSY * self.zoom)
        targetX = w/2 + targ_dx + (self.panX * self.zoom)
        targetY = h/2 + targ_dy + (self.panY * self.zoom)
        targetDirection = atan2(-(targetGpsY - userGpsY), targetGpsX - userGpsX)
        
        # draw line between user and target
        (x, y) = (userX, userY)
        remaining = sqrt(pow(targetX - userX, 2) + pow(targetY - userY, 2))
        dashLength = 10
        while (remaining > dashLength):
            theta = atan2(targetY - y, targetX - x)
            app.body.line([(x,y), (x + dashLength*cos(theta), y + dashLength*sin(theta))], outline = mmm_color.GOLD, width = 2)
            remaining = remaining - 2 * dashLength
            x = x + 2.0 * dashLength*cos(theta)
            y = y + 2.0 * dashLength*sin(theta)
        #app.body.line([(userX, userY), (targetX, targetY)], outline = mmm_color.GOLD, width = 2)
        
        # draw user
        (iconW, iconH) = userIcon.size
        app.body.blit(userIcon, mask = userIcon_mask, target = (userX - iconW/2, userY - iconH/3))
        
        # draw target        
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
        
        # draw pan arrows
        app.body.polygon(self.upVertices, outline = mmm_color.BLACK, fill = mmm_color.WHITE, width = 2) 
        app.body.polygon(self.downVertices, outline = mmm_color.BLACK, fill = mmm_color.WHITE, width = 2)
        app.body.polygon(self.leftVertices, outline = mmm_color.BLACK, fill = mmm_color.WHITE, width = 2) 
        app.body.polygon(self.rightVertices, outline = mmm_color.BLACK, fill = mmm_color.WHITE, width = 2) 
        #setCoords(vertices, (106, 9)), 
            
        # if both user and target are offscreen, draw arrows indicating position on map     
        if (not(userX >= -iconW/2 and userX < w + iconW/2 and userY >= -iconH/3 and userY < h + iconH/3)
            and not(targetX >= -targW/2 and targetX < w + targW/2 and targetY >= -targH/2 and targetY < h + targH/2)):
            arrowRadius = targW/2
            userArrowLoc = self.computeArrowLocation((w/2, h/2), (userX, userY), arrowRadius)
            targetArrowLoc = self.computeArrowLocation((w/2, h/2), (targetX, targetY), arrowRadius)
            (self.userArrow.x, self.userArrow.y) = userArrowLoc
            (self.targetArrow.x, self.targetArrow.y) = targetArrowLoc
            self.userArrow.theta = atan2(userY - h/2, userX - w/2)
            self.targetArrow.theta = atan2(targetY - h/2, targetX - w/2)
            self.userArrow.draw(app.body)
            self.targetArrow.draw(app.body)
            
        # draw signal strength               
        #app.body.blit(onebarsIcon, mask = onebarsIcon_mask, target = (184, 2))
        #app.body.blit(twobarsIcon, mask = twobarsIcon_mask, target = (184, 2))
        #app.body.blit(threebarsIcon, mask = threebarsIcon_mask, target = (184, 2))
        #app.body.blit(fourbarsIcon, mask = fourbarsIcon_mask, target = (184, 2))
        app.body.blit(fivebarsIcon, mask = fivebarsIcon_mask, target = (184, 2))
        
        # draw map ui controls
        app.body.blit(self.overlay, mask = self.overlay_mask) 
    
if __name__ == "__main__":
    map = MapUI()