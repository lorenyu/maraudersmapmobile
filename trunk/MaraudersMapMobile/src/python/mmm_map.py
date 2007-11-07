from appuifw import *
from graphics import *

class Map:
    def __init__(self):
        try:
            print "Loading map image"
            self.image = Image.open("C:\\Data\\Images\\tressider2-medquality.jpg")
            # read this in from text file - can eval(text), and then have a dictionary
            print "Loading map coords"
            f = file(u"C:\\Data\\Others\\tressider2-coords.txt", "r")
            str = ""
            for line in f:
                str += line.strip()
            f.close()
            mapCoords = eval(str)		
            self.coords = mapCoords
            print "Map coords: ", self.coords
        except Exception, e:
            print e
        print "Map constructor"
        
if __name__ == "__main__":
    map = Map()