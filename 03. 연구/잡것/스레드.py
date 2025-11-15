import threading
import time

def tc():
    while 1:
        print('!')
        time.sleep(0.02)
        
t = threading.Thread(target = tc)
t.start()

for i in range(100):
    print(i)
