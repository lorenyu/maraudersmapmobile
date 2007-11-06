#
# gps.py
#

import positioning
import appuifw, e32

# SYMBIAN_UID = 0xE1000121

def updatePosition(event):
    positionInfo = event['position']
    courseInfo = event['course']
    print 'lat: ', positionInfo['latitude']
    print 'lon: ', positionInfo['longitude']
    #print '(lat,lon) = (%.3f, %.3f)' %(positionInfo['latitude'], positionInfo['longitude'])
    #print 'heading = %.3f' %(courseInfo['heading'])

def quit():
    print "Stopping GPS"
    positioning.stop_position()
    print "Exiting app"
    app_lock.signal()
    
# set requestors.
# at least one requestor must be set before requesting the position.
# the last requestor must always be service requestor 
positioning.set_requestors([{"type":"service",
                             "format":"application",
                             "data":"test_app"}])

#
# pos = positioning.position(course=1,interval=[time in microseconds],callback=[callback])
# pos.position = {
#       'latitude' : ----
#       'longitude' : ----
#       'altitude' : ----
#       'horizontal_accuracy' : ---- }
#
# pos.course = {
#       'heading' : ----
#       'heading_accuracy' : ---- }
                             
# get the position. 
# note that the first position()-call may take a long time
# (because of gps technology).
print "Getting position info"
positioning.position(course = 1, callback = updatePosition, interval = 500000)

appuifw.app.exit_key_handler = quit
app_lock = e32.Ao_lock()
app_lock.wait()
