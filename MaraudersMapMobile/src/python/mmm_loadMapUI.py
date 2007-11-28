# mmm_loadMapUI.py

from appuifw import *
from e32 import *
from graphics import *
from mmm_utils import *

class LoadMapUI:
    def __init__(self):
        self.image = Image.open("C:\\Data\\Images\\loadingMap.jpg")
        self.menu = []
        self.timer = Ao_timer()
        self.lock = Ao_lock()
        
    def run(self):
        def quit():
            self.timer.cancel()
            self.lock.signal()
            
        def redraw(rect):
            app.body.blit(self.image)
        
        def loadMap():
            app.mapUI.run()
            self.lock.signal()
        
        saveState()
        app.screen = 'full'
        app.menu = self.menu
        app.redraw = redraw
        app.redraw(None)
        app.exit_key_handler = quit
        
        self.timer.after(3, loadMap)
        self.lock.wait()
        restoreState()