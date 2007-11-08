import appuifw, colorMod, operator
from graphics import *
from math import sin, cos, pi

def drawIcons(canvas, targetLoc, arrowLoc):
	addUserIcon(canvas)
	drawTargetIcon(canvas, targetLoc)
	drawArrowIcon(canvas, arrowLoc, deltaTheta)
	
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

#def drawArrowIcon(canvas, arrowLoc):
 #       cx = arrowLoc.x
  #      cy = arrowLoc.y
   #     iconOffsets = getArrowIconOffsets()
    #    vertices = []
        
        #testCoords = map(rotate, getArrowIconOffsets())
        
     #   for i in range(0, 7):
      #          vertices.append(((cx + iconOffsets[i][0]), (cy + iconOffsets[i][1])))
        
       # canvas.polygon(vertices, outline = colorMod.BLACK, fill = colorMod.GREEN, width = 2)
        
        #INSERT TEXT HERE (CALLEE'S NAME):)


def drawArrowIcon(canvas, arrowLoc, theta): #theta or delta theta?
        cx = arrowLoc.x
        cy = arrowLoc.y
        iconOffsets = getArrowIconOffsets()
        finalVertices = []
        for j in range(0, 7):
                finalVertices.append( (( iconOffsets[j][0] * cos(theta) -  iconOffsets[j][1] * sin(theta)), ( iconOffsets[j][1] * cos(theta) + iconOffsets[j][0]* sin(theta)) ))

        for i in range(0, 7):
                finalVertices[i] = (((cx + finalVertices[i][0]), (cy + finalVertices[i][1])))
        
        canvas.polygon(finalVertices, outline = colorMod.BLACK, fill = colorMod.GREEN, width = 2)

        
def getUserIconOffsets():
	return [(-10, 14), (0, -14), (10, 14), (0, 8)]
	
def getTargetIconOffsets():
	return[(-14, 21), (-9, 4), (-21, -5), (-5, -5), (0, -23), (5, -5),
		(21, -5), (9, 4), (14, 21), (0, 12)]

def getArrowIconOffsets(): 
        return [(-25, 6), (-25, -6), (4, -6), (4, -13), (25, 1), (4, 13), (4, 6)]

def rotate((x, y)):
        return (( (x * cos(pi) - y * sin(pi)), (y * cos(pi) + x * sin(pi)) ))
        
			
