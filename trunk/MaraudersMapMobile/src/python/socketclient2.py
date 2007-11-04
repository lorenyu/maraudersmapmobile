import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = "128.12.93.14" # phone ip
#ip = "127.0.0.1" # localhost
#ip = "128.12.95.144" # desktop
#ip = "FENIX8" # desktop
print "Connect to " + ip
s.connect((ip, 3000))
print "Done"