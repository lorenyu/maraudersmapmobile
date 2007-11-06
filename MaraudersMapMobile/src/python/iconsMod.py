import appuifw, colorMod
from graphics import *

def drawIcons(canvas, targetLoc):
	addUserIcon(canvas)
	drawTargetIcon(canvas, targetLoc)
	
def addUserIcon(canvas):
	w, h = canvas.size
	canvasMidX = w/2
	canvasMidY = h/2
	iconOffsets = getUserIconOffsets()
	vertices = []
	for i in range(0, 4):
		vertices.append(((canvasMidX + iconOffsets[i][0]), (canvasMidY + iconOffsets[i][1])))
	
	canvas.polygon(vertices, outline = colorMod.BLACK, fill = colorMod.RED, width = 2) 
	canvas.text((canvasMidX - 10, canvasMidY + 30), u"You", fill = colorMod.WHITE)

def drawTargetIcon(canvas, targLoc):
	cx = targLoc.x
	cy = targLoc.y
	iconOffsets = getTargetIconOffsets()
	vertices = []
	for i in range(0, 10):
		vertices.append(((cx + iconOffsets[i][0]), (cy + iconOffsets[i][1])))
	canvas.polygon(vertices, outline = colorMod.BLACK, fill = colorMod.GREEN, width = 2) 
	canvas.text((cx - 14, cy + 37), u"Andy", fill = colorMod.WHITE)

def getUserIconOffsets():
	return [(-10, 14), (0, -14), (10, 14), (0, 8)]
	
def getTargetIconOffsets():
	return[(-14, 21), (-9, 4), (-21, -5), (-5, -5), (0, -23), (5, -5),
		(21, -5), (9, 4), (14, 21), (0, 12)]
			
