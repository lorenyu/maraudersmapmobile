from appuifw import *
from e32 import *
from graphics import *
from mmm_talkingUI import *
from mmm_mapUI import *
from mmm_receivedLocationUI import *
from mmm_loadMapUI import *

allowShare = False 

app.redraw = None
app.keyBindings = None

def redraw(rect):
    if (app.redraw != None):
        app.redraw(rect)

app.mapUI = MapUI()
app.talkingUI = TalkingUI()
app.receivedLocationUI = ReceivedLocationUI()
app.loadMapUI = LoadMapUI()

app.body = Canvas(redraw_callback = redraw)
app.talkingUI.run()