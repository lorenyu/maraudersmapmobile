# Copyright (c) 2006 Jurgen Scheible
# image download

import appuifw
import e32
import urllib


def main_menu_setup():
    appuifw.app.menu = [(u"get picture", get_picture), (u"get video", fetching)]


def get_picture():
    url = "http://www.leninsgodson.com/courses/pys60/resources/pic001.jpg"
    tempfile = "c:\\picture01.jpg"
    urllib.urlretrieve(url, tempfile)
    lock=e32.Ao_lock()
    content_handler = appuifw.Content_handler(lock.signal)
    content_handler.open(tempfile)
    lock.wait()



def fetching():
    url = "http://www.leninsgodson.com/courses/pys60/resources/vid001.3gp"
    tempfile = "c:\\video01.3gp"
    try:
        print "Retrieving information..."
        urllib.urlretrieve(url, tempfile)
        lock=e32.Ao_lock()
        content_handler = appuifw.Content_handler(lock.signal)
        content_handler.open(tempfile)
        # Wait for the user to exit the image viewer.
        lock.wait()
        print "Video viewing finished."
    except IOError:
        print "Could not fetch the image."
    except:
        print "Could not open data received."


def exit_key_handler():
    global script_lock
    script_lock.signal()
    appuifw.app.set_exit()
    

script_lock = e32.Ao_lock()

appuifw.app.title = u"Get pic & vid"

appuifw.app.body = appuifw.Text(u"Press Options button below ...")

main_menu_setup()
appuifw.app.exit_key_handler = exit_key_handler
script_lock.wait()


 

