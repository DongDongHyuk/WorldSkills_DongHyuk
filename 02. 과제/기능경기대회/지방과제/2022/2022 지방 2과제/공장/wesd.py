import random as r
import time as t
X = -99
C__ = [[X,X,X,X,X],
     [X,0,0,0,X],
     [X,0,0,0,X],
     [X,0,0,0,X],
     [X,X,X,X,X]]
log = []
def print_(li):
    ee = []
    for y in range(1,4):
        for x in range(1,4):
            ee.append(li[y][x])
    return ee
li_copy = lambda li : list(map(lambda f:f[:],li))
def start():
    global log
    S_1 = []
    S_2 = []
    while 1:
        yww = r.randint(1,3)
        xww = r.randint(1,3)
        if yww == xww == 2:
            continue
        for b in range(2):
            C__ = [[X,X,X,X,X],
                 [X,0,0,0,X],
                 [X,0,0,0,X],
                 [X,0,0,0,X],
                 [X,X,X,X,X]]
            C__[yww][xww] = 3
            for i in [1,2]:
                while 1:
                    y = r.randint(1,3)
                    x = r.randint(1,3)
                    if not C__[y][x]:
                        C__[y][x] = i
                        break
            if not b:
                for e in [1,1,2,2]:
                    for y in range(1,4):
                        for x in range(1,4):
                            if C__[y][x] == 0:
                                C__[y][x] = e
                                break
                        else:continue
                        break
                log.append(C__)
                S_1 = print_(C__)
                print(' ')
            if b:
                while 1:
                    C__1 = li_copy(C__)
                    for e in [2,2,1,1]:
                        while 1:
                            y = r.randint(1,3)
                            x = r.randint(1,3)
                            if not C__1[y][x]:
                                C__1[y][x] = e
                                break
                    if log[0] == C__1:
                        continue
                    else:
                        S_2 = print_(C__1)
                        log = []
                        break
        else: break    
    return S_2,S_1
    
