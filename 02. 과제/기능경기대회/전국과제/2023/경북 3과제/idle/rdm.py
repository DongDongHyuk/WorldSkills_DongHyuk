import random
from printer import printf
def rdm(t):
    res = []
    c = random.choice
    rdp = lambda m,li=-1: c([i for i in (range(len(m)) if li is -1 else li) if m[i] is '0'])
    if t == 0:
        for i in range(2):
            m = list('0x0xx0x0')+list('0'*8)
            for j in '12345678':
                pos = rdp(m,list(range(8,16))) if i else rdp(m)
                m[pos] = j
            res.append(''.join(m))
    if t == 1:
        xp = c([2,10,14,22])
        for i in range(2):
            m = list('xx0xxx000x00x00x000xxx0xx')
            m[xp] = 'x'
            for j in '12345678':
                pos = rdp(m,[k for k in range(25) if k not in [2,10,14,22]]) if i else rdp(m)
                m[pos] = j
            res.append(''.join(m))
    if t == 2:
        res = []
        xli = []
        hli = []
        fix = []
        for _ in range(3):
            n = c([i for i in range(16) if i not in fix+xli])
            xli.append(n)
            y,x = divmod(n,4)
            for dy,dx in zip([-1,-1,0,1,1,1,0,-1],[0,1,1,1,0,-1,-1,-1]):
                ny,nx = y + dy,x + dx
                if -1 < ny < 4 and -1 < nx < 4:
                    fix.append(ny * 4 + nx)
        for _ in range(2):
            hli.append(c([i for i in range(16) if i not in xli+hli]))
        for i in range(2):
            m = list('0'*16)
            for j in xli:
                m[j] = 'x'
            for j in '12345678':
                n = c([i for i in range(16) if m[i] is '0' and i not in hli])
                m[n] = j
            res.append(''.join(m))
        res.append(hli)
    return res
