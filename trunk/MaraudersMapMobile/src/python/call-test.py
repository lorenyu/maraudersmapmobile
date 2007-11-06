# call-test.py

import telephone

def answer_call((new_state, number)):
    print "New state", new_state
    print "Call from ", number
    if (new_state == telephone.EStatusRinging):
        print "Answered call"
        telephone.answer()

for i in dir(telephone):
    print i
    
telephone.incoming_call()

telephone.call_state(answer_call)

import appuifw, e32
def quit():
    print "Exiting app"
    app_lock.signal()

print telephone.EStatusRinging

def doNothing():
    appuifw.note(u"Sorry can't do that!")

def shareLocation():
    swfLock = e32.Ao_lock()
    swfLoader = appuifw.Content_handler(swfLock.signal)
    swfLoader.open("E:\\Others\\App.swf")
    swfLock.wait()
    #e32.start_exe("E:\\Others\\App.swf", "")
    #appuifw.note(u"Location shared")

canvas = appuifw.Canvas()
appuifw.app.body = canvas
appuifw.app.exit_key_handler = quit
appuifw.app.menu = [
    (u"Mute", doNothing),
    (u"Loud Speaker", doNothing),
    (u"Hold", doNothing),
    (u"Share Location", shareLocation)]
    
app_lock = e32.Ao_lock()
app_lock.wait()