import appuifw, e32, mapMod, userLocMod, targetLocMod, colorMod, iconsMod
from graphics import *

def quit():
    app_lock.signal()

canvas = appuifw.Canvas()
appuifw.app.body = canvas
appuifw.app.exit_key_handler = quit

map = mapMod.Map()
userLoc = userLocMod.UserLoc(1005, 1075, 90)
targetLoc = targetLocMod.TargetLoc(130, 200)

canvas.blit(map.image)
iconsMod.drawIcons(canvas, targetLoc)

app_lock = e32.Ao_lock()
app_lock.wait()