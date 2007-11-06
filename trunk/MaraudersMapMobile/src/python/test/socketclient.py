# socketclient.py

from socket import *

serverHost = '128.12.95.128'
serverPort = 7777

s = socket(AF_INET, SOCK_STREAM)
s.connect((serverHost, serverPort))
s.send('William Shakespeare')
print s.recv(9999)
s.close()