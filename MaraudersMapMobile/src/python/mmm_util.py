from appuifw import *

def saveAppState():
    global body
    global exit
    global title
    global menu
    print "Saving app state"
    body = app.body
    exit = app.exit_key_handler
    title = app.title
    menu = app.menu
    
def restoreAppState():
    print "Restoring app state"
    app.body = body
    app.exit_key_handler = exit
    app.title = title
    app.menu = menu
