from appuifw import *
from e32 import *

def doNothing():
    note(u"Sorry can't do that!")

def quit():
    app_lock.signal()

def init():
    app.body = canvas
    app.exit_key_handler = quit
    app.title = u"PhotoEditor"
    app.menu = options
    
canvas = Canvas()
title = u"Talking"
options = [
    (u"Zoom in (*)", doNothing),
    (u"Zoom out (#)", doNothing),
    (u"Satellite info", doNothing)]
app_lock = Ao_lock()

if __name__ == "__main__":
    init()
    app_lock.wait()