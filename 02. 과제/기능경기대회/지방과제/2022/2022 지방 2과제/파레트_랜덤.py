import random as r
X = -99
C__ = [[X,X,X,X,X],
     [X,0,0,0,X],
     [X,0,0,0,X],
     [X,0,0,0,X],
     [X,X,X,X,X]]
log = []
def print_(li):
    for y in range(1,4):
        for x in range(1,4):
            print(str(li[y][x])+',',end='')
    print(' ')
li_copy = lambda li : list(map(lambda f:f[:],li))
while 1:
    yww = r.randint(1,3)
    xww = r.randint(1,3)
    if yww == xww == 2:
        continue
    input('')
    print('=================')
    print('=================')
    print('=================')
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
            print_(C__)
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
                    print_(C__1)
                    log = []
                    break
    
