from rd import *
import main
import time

ct = 0
mx,mn = 0,0
while 1:
    m = getbr()
    print('map :',m)
    ts = time.time()
    res = main.main(m)
    te = time.time() - ts
    if mx < te:
        mx = te
    if mn > te:
        mn = te
    print('step :',res)
    print('now : {}, min : {}, max : {}'.format(te,mn,mx))
    print(ct)
    ct += 1
