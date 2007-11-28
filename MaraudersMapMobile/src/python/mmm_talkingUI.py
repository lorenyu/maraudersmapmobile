# mmm_talkingUI.py

from appuifw import *
from e32 import *
from graphics import *
from mmm_utils import *

def receiveLocation():
    ao_sleep(3)
    app.receivedLocationUI.run()
    app.redraw(None)
    
def shareLocation():
    app.loadMapUI.run()
    app.redraw(None)
    
class TalkingUI:
    def __init__(self):
    
        self.talking_title = "Talking"
        self.talking_image = Image.open("C:\\Data\\Images\\talking1.jpg")
        self.talking_menu = [
            (u"Mute", receiveLocation),
            (u"Loud Speaker", doNothing),
            (u"Hold", doNothing),
            (u"Share Location", shareLocation)]
        self.talking_lock = Ao_lock()
        self.loadingMap_image = Image.open("C:\\Data\\Images\\loadingMap.jpg")

    def run(self):
        def talking_quit():
            self.talking_lock.signal()
            
        def talking_redraw(rect):
            app.body.blit(self.talking_image)
            
        saveState()
        app.screen = 'normal'
        app.menu = self.talking_menu
        app.redraw = talking_redraw
        app.redraw(None)
        app.exit_key_handler = talking_quit
        self.talking_lock.wait()
        restoreState()
        
# Prompting
#receivedLocation_image = Image.open("C:\\Data\\Images\\promptingToShare.jpg")
#receivedLocation_menu = [(u"Confirm", temp)]


#loadingMap_menu = [
#    (u"Mute", doNothing),
#    (u"Loud Speaker", doNothing),
#    (u"Hold", doNothing)]

