# mmm_gps.py
import positioning
from e32 import *

PIXELS_PER_GPSX = 186220
PIXELS_PER_GPSY = -234192

GPSX_PER_PIXEL = 0.00000537
GPSY_PER_PIXEL= -0.00000427

# hardcode target's coords
targetGpsX = -122.173424
targetGpsY = 37.430778

# if GPS not working, hardcode user's coords
# Gates GPS coords
userGpsX = -122.173156
userGpsY = 37.429900
# Tressider 
#userGpsX = -122.170715
#userGpsY = 37.424196

def updatePosition(event):
    global userGpsX
    global userGpsY
    positionInfo = event['position']
    courseInfo = event['course']
    userGpsY = positionInfo['latitude']
    userGpsX = positionInfo['longitude']

if (not(in_emulator())):
    positioning.set_requestors([{
        "type" : "service",
        "format" : "application",
        "data"   : "test_app"}])
    positioning.position(course = 1, callback = updatePosition, interval = 500000)