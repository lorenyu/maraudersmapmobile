from math import sin, cos, pi
import appuifw, colorMod, operator
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
        self.offsets = [(-25, 6), (-25, -6), (4, -6), (4, -13), (25, 1), (4, 13), (4, 6)]
        self.radius = 29
                

    
    def draw(self, canvas): #theta or delta theta?
        cx = self.x
        cy = self.y
        iconOffsets = self.offsets
        finalVertices = []
        for j in range(0, 7):
            finalVertices.append( rotate(iconOffsets[j], self.theta ) )

        for i in range(0, 7):
            finalVertices[i] = (((cx + finalVertices[i][0]), (cy + finalVertices[i][1])))
        
        canvas.polygon(finalVertices, outline = colorMod.BLACK, fill = colorMod.GOLD, width = 2)
        canvas.ellipse(circleCoords(self.x, self.y, self.radius-1), outline = colorMod.GOLD, width = 2)
        canvas.ellipse(circleCoords(self.x, self.y, self.radius), outline = colorMod.BLACK, width = 2)
        
