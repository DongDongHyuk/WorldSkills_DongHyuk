from socket import *
import time


Sock = socket(AF_INET, SOCK_STREAM)
while 1:
    try:
        Sock.connect(('192.168.137.100',20001))
    except:
        time.sleep(0.1)
        print('.')
        continue
    else: break
Sock.send(bytes(str(None),'utf-8'))
n = eval(Sock.recv(1024).decode('utf-8'))
print(n)

