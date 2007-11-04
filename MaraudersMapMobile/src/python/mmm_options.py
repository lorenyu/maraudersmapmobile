import appuifw, e32

def doNothing():
    appuifw.note(u"Sorry can't do that!")

def shareLocation():
    swfLock = e32.Ao_lock()
    swfLoader = appuifw.Content_handler(swfLock.signal)
    swfLoader.open("E:\\Others\\App.swf")
    swfLock.wait()
    #e32.start_exe("E:\\Others\\App.swf", "")
    #appuifw.note(u"Location shared")

def quit():
    app_lock.signal()

canvas = appuifw.Canvas()
appuifw.app.body = canvas
appuifw.app.exit_key_handler = quit
appuifw.app.title = u"PhotoEditor"
appuifw.app.menu = [
    (u"Mute", doNothing),
    (u"Loud Speaker", doNothing),
    (u"Hold", doNothing),
    (u"Share Location", shareLocation)]

app_lock = e32.Ao_lock()
app_lock.wait()
