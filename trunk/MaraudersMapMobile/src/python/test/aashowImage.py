from appuifw import *
from e32 import *
from graphics import *
from mmm_map import *
from key_codes import *
from arrowLocMod import *
from math import sin, cos, pi, atan2

def setImage1():
    global image
    image = image1

def setImage2():
    global image
    image = image2


def redraw(rect):
    canvas.blit(image)
    
def quit():
    app_lock.signal()
    
    
image1 = Image.open("C:\\Data\\Images\\talking1.jpg")
image2 = Image.open("C:\\Data\\Images\\loadingMap.jpg")

image = image1

canvas = Canvas(redraw_callback = redraw)

app.menu = [(u'Image 1', setImage1), (u'Image 2', setImage2)]
app.body = canvas
app.exit_key_handler = quit
app_lock = Ao_lock()
app_lock.wait()