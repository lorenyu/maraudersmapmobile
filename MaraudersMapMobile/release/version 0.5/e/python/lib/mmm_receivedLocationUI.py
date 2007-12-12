# mmm_receivedLocationUI.py

from appuifw import *
from e32 import *
from key_codes import *
from graphics import *
from mmm_utils import *
    
class ReceivedLocationUI:
    def __init__(self):
        def loadMap():
            app.loadMapUI.run()
            self.lock.signal()
            
        self.keyBindings = {
            EKeySelect : loadMap}
        self.image = Image.open("C:\\Data\\Images\\promptingToShare.jpg")
        self.menu = [(u"Confirm", loadMap)]
        self.lock = Ao_lock()

    def run(self):
        def quit():
            self.lock.signal()
            
        def redraw(rect):
            app.body.blit(self.image)
            
        saveState()
        setKeyBindings(self.keyBindings)
        
        app.screen = 'full'
        app.menu = self.menu
        app.redraw = redraw
        app.redraw(None)
        app.exit_key_handler = quit
        self.lock.wait()
        restoreState()
        

