from math import sin, cos, pi
import appuifw, mmm_color
from graphics import *

def circleCoords(x, y, radius):
    topLeft = (x - radius, y - radius)
    bottomRight = (x + radius, y + radius)
    return [topLeft, bottomRight]
        
def rotate( (x, y) , theta):
    return ( x * cos(theta) - y * sin(theta), x * sin(theta) + y * cos(theta) )
        
class TargetArrow:
    #Name = "TargetArrow"
    
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.theta = dir
        self.color = mmm_color.RED
        #self.offsets = [(-25, 6), (-25, -6), (4, -6), (4, -13), (25, 0), (4, 13), (4, 6)]
        self.offsets = [(-25, 8), (-25, -8), (0, -8), (0, -18), (25, 0), (0, 18), (0, 8)]
        self.radius = 29
        self.isCircleVisible = True

    def setScale(self, scale):
        def scaleCoord((x, y)):
            return (x * scale, y * scale)
        self.offsets = map(scaleCoord, self.offsets)
        self.radius = self.radius * scale
    
    def draw(self, canvas): #theta or delta theta?
        cx = self.x
        cy = self.y
        iconOffsets = self.offsets
        finalVertices = []
        for j in range(0, 7):
            finalVertices.append( rotate(iconOffsets[j], self.theta ) )

        for i in range(0, 7):
            finalVertices[i] = (((cx + finalVertices[i][0]), (cy + finalVertices[i][1])))
        
        canvas.polygon(finalVertices, outline = mmm_color.BLACK, fill = self.color, width = 2)
        if (self.isCircleVisible):
            canvas.ellipse(circleCoords(self.x, self.y, self.radius-1), outline = mmm_color.GOLD, width = 2)
            canvas.ellipse(circleCoords(self.x, self.y, self.radius), outline = mmm_color.BLACK, width = 2)
        
