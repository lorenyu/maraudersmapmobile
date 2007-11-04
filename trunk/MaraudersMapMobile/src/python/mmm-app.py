from appuifw import *
from e32 import *

menu = [
    (u"Mute", doNothing),
    (u"Loud Speaker", doNothing),
    (u"Hold", doNothing),
    (u"Share Location", shareLocation)]

def doNothing():
    note(u"Sorry can't do that!")

def shareLocation():
    note

def quit():
    app_lock.signal()

if __name__ == "__main__":
    canvas = Canvas()
    app.body = canvas
    app.exit_key_handler = quit
    app.title = u"Marauder's Map Mobile"
    app.menu = menu

    app_lock = Ao_lock()
    app_lock.wait()
