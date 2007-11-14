# socketclient.py

from socket import *

serverHost = '128.12.95.128'
serverPort = 7777

s = socket(AF_INET, SOCK_STREAM)
s.connect((serverHost, serverPort))
while True:
    message = s.recv(9999)
    print "Received message: ", message
    if (message == "prompt to share"):
        promptToShare()
        #break
    if (message == "quit"):
        break

print "Closing connection"
s.close()
print "Closing application"

def promptToShare():
    print "in prompt to share method"
    #   now have to call mmm_functional's code to load appropriate screen
    # or will this all be in mmm_functional