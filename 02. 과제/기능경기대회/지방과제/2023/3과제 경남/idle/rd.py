from random import *

def getbr():
    s,e = 1,21
    li = [0,0,0,0,0,0,0,0]
    for i in range(6):
        nl = [j for j in range(8) if li[j] == 0]
        s = [1,21,41,61,81,91][i]
        e = [21,41,61,81,91,100][i]
        num = choice(list(range(s,e)))
        li[choice(nl)] = num
    return li
