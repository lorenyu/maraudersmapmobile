from e32 import *
from appuifw import *

timer = Ao_timer()
cancelled = False

def done():
    print "timer done"
    app_lock.signal()

def cancel():
    global cancelled
    print "cancelling timer"
    cancelled = True
    timer.cancel()
    app_lock.signal()
    print "timer cancelled"

app.exit_key_handler = cancel
print "start timer"
timer.after(3, done)

app_lock = Ao_lock()
app_lock.wait()
print "exiting"
