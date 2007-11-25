#
# mmm-gps.py
#

import positioning


positioning.set_requestors([{
    "type" : "service",
    "format" : "application",
    "data"   : "test_app"}])
positioning.position(course = 1, callback = updatePosition, interval = 500000)

    def updatePosition(event):
        positionInfo = event['position']
        courseInfo = event['course']
        print '(lat,lon) = (%.3f, %.3f)' %(positionInfo['latitude'], positionInfo['longitude'])
        print 'heading = %.3f' %(courseInfo['heading'])
        # ----Marcia's code starts here!----
        print 'horizontal_accuracy = %.3f' %(positionInfo['horizontal_accuracy'])
        # ----Marcia's code ends here!----


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

appuifw.app.exit_key_handler = quit
app_lock = e32.Ao_lock()
app_lock.wait()
