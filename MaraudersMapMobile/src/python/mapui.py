import appuifw, e32
from graphics import *

WHITE = (255, 255, 255)
RED = (255,0,0)  
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

map = Image.open("C:\\Data\\Images\\tressider-lowquality.jpg")
gpsXMin = None
gpsYMin = None
gpsXMax = None
gpsYMax = None

gpsX = None
gpsY = None
compassDirection = None

targetX = None
targetY = None

canvasW = None
canvasH = None

def quit():
    app_lock.signal()

def initMap():
	gpsXMin = 0
	gpsYMin = 0
	gpsXMax, gpsYMax = map.size

def initPeopleLoc():
	gpsX = 1005
	gpsY = 1075
	compassDirection = 90
	# compDirection convention changed?
	targetX = 798
	targetY = 1143
	
def addUserIcon():
	map.polygon([(canvasW/2 - 10, canvasH/2 + 14),
		(canvasW/2, canvasH/2 - 14),
		(canvasW/2 + 10, canvasH/2 + 14), 
		(canvasW/2, canvasH/2 + 8)], outline = BLACK, fill = RED, width = 2) 
	map.text((canvasW/2 - 10, canvasH/2 + 30), u"You", fill = WHITE)
		

def drawTargetIcon(cx, cy):
	map.polygon([(cx - 14, cy + 21),
		(cx - 9, cy + 4),
		(cx - 21, cy - 5),
		(cx - 5, cy - 5),
		(cx, cy - 23),
		(cx + 5, cy - 5),
		(cx + 21, cy - 5),
		(cx + 9, cy + 4),
		(cx + 14, cy + 21),
		(cx, cy + 12)], outline = BLACK, fill = GREEN, width = 2) 
	map.text((cx - 14, cy + 37), u"Andy", fill = WHITE)

canvas = appuifw.Canvas()
appuifw.app.body = canvas
appuifw.app.exit_key_handler = quit

canvasW, canvasH = canvas.size

initMap()
initPeopleLoc()
addUserIcon()

cx = canvasW/2
cy = canvasH/2 + 50
drawTargetIcon(cx, cy)

canvas.blit(map)

app_lock = e32.Ao_lock()
app_lock.wait()