# mmm_utils.py

from appuifw import *

oldState = []

def saveState():
    oldState.append((
        app.menu,
        app.redraw,
        app.exit_key_handler,
        app.screen,
        app.keyBindings))
    
def restoreState():
    if (len(oldState) <= 0):
        return
        
    # erase current key bindings
    if (app.keyBindings != None):
        for key in app.keyBindings.keys():
            app.body.bind(key, None)
            
    (app.menu, app.redraw, app.exit_key_handler, app.screen, app.keyBindings) = oldState.pop()
    
    # restore previous key bindings
    if (app.keyBindings != None):
        for key in app.keyBindings.keys():
            app.body.bind(key, app.keyBindings[key])
        
def setKeyBindings(keyBindings):
    for key in keyBindings.keys():
        app.body.bind(key, keyBindings[key])
    app.keyBindings = keyBindings
    

def doNothing():
    print "do nothing"