from random import choice as c, sample as cs
from Printer import prt

def randomMap(t):
    res = []
    if t == 0:
        m = ['0']*16
        for pk in '123456789a':
            p = c([i for i in range(16) if m[i] == '0'])
            m[p] = pk
        res.append(''.join(m))
    if t == 1:
        pass
    if t == 2:
        pass
    return res