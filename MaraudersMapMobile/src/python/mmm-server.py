# socketserver.py

from socket import *
from Tkinter import *

# Socket server variables
serverHost = '0.0.0.0'
serverPort = 7777
maxConnections = 9999
connection = None

# Application variables
root = Tk()

direction = "north"

def sendDirection():
    print "Sending ", direction
    connection.send(direction)

def north():
    global direction
    direction = "north"
    sendDirection()
    
def south():
    global direction
    direction = "south"
    sendDirection()
    
def east():
    global direction
    direction = "east"
    sendDirection()
    
def west():
    global direction
    direction = "west"
    sendDirection()
    
def quit():
    print "Closing connection"
    connection.send("quit")
    connection.close()
    print "Exiting application"
    root.quit()
    
keymap = {
    87  : north, # W
    65  : west,  # A
    83  : south, # S
    68  : east,  # D
    27  : quit}  # Esc

# Keyboard handler
def key(event):
    if (keymap.has_key(event.keycode)):
        keymap[event.keycode]()

# Mouse handler
def mouse(event):
    frame.focus_set()
    
# 
# Start socket server
# 

print "Starting socket server"
s = socket(AF_INET, SOCK_STREAM)
s.bind((serverHost, serverPort))
s.listen(maxConnections)

# Waiting for connection
print "Waiting for connection"
(connection, address) = s.accept()
print "Connected to ", address

#
# Create GUI
#

print "Building UI"
frame = Frame(root, width=100, height=100)
frame.bind("<Key>", key)
frame.bind("<Button-1>", mouse)
frame.pack()
frame.focus_set()

root.mainloop()