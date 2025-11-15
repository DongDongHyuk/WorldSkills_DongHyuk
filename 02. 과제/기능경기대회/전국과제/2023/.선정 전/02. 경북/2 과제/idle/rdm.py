import random
from printer import printf

def rdm(t):
    c = random.choice
    rdp = lambda m: c([i for i in range(len(m)) if m[i] is '0'])
    if t is 0:
        m = list('x0x000000000x0x')
        for i in 'abcdefgh':
            n = rdp(m)
            m[n] = i
        res = [''.join(m),c([1,2,3,4])]
    if t is 1:
        m = list('0'*12)
        m[c([4,5,6,7])] = 'x'
        for i in 'ijklmnop':
            n = rdp(m)
            m[n] = i
        res = ''.join(m)
    if t is 2:
        fix = []
        m = list('0'*16)
        for _ in range(4):
            n = c([i for i in range(len(m)) if m[i] is '0' and i not in fix])
            m[n] = 'x'
            y,x = divmod(n,4)
            for dy,dx in zip([-1,-1,0,1,1,1,0,-1],[0,1,1,1,0,-1,-1,-1]):
                ny,nx = y + dy,x + dx
                if -1 < ny < 4 and -1 < nx < 4:
                    fix.append(ny * 4 + nx)
        for i in 'qrstuvwyz':
            n = rdp(m)
            m[n] = i                
        res = ''.join(m)
    return res
