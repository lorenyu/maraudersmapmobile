from appuifw import *
from graphics import *
from e32 import *

class Map:
    def __init__(self):
        try:
            print "Loading map image"
            self.image = Image.open("C:\\Data\\Images\\gates_000.jpg")
            self.orig_image = self.image
            self.zoom = 1
            self.x = 0
            self.y = 0
            self.overlay = Image.open("C:\\Data\\Images\\mapui1.jpg")
            self.overlay_mask = Image.new(self.overlay.size, mode = 'L')
            self.overlay_mask.blit(Image.open("C:\\Data\\Images\\mapui1_mask.jpg"))
            
            print "Loading map coords"
            f = file(u"C:\\Data\\Others\\gates_coords.txt", "r")
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