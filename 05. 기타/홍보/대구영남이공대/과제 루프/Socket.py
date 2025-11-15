from socket import *
from calculation_part import main
import time

while 1: 
    Sock = socket(AF_INET, SOCK_STREAM)
    while 1:
        try:
            Sock.connect(('192.168.137.100',20001))
        except:
            print('.')
            continue
        else:break
    try:
        root = eval(Sock.recv(1024).decode('utf-8')) #읽기
        print('Calculating...',end = '')
        result = main(root)[:]
        print('Completed !!!')
        Sock.send(bytes(str(result),'utf-8')) # 쓰기
    except: continue
