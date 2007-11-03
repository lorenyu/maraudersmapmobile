import appuifw, e32
from graphics import *

def quit():
    app_lock.signal()

map = Image.open("C:\\Data\\Images\\tressider-lowquality.jpg")
print dir(map)

canvas = appuifw.Canvas()
appuifw.app.body = canvas

appuifw.app.exit_key_handler = quit



canvas.blit(map)

app_lock = e32.Ao_lock()
app_lock.wait()