# socketserver.py

from socket import *

serverHost = '0.0.0.0'
serverPort = 7777
numConnections = 2

s = socket(AF_INET, SOCK_STREAM)
s.bind((serverHost, serverPort))
s.listen(numConnections)

while (numConnections > 0):
    (connection, address) = s.accept()
    print connection.recv(9999)
    connection.send('Green-eyed monster.')
    connection.close()
    numConnections = numConnections - 1