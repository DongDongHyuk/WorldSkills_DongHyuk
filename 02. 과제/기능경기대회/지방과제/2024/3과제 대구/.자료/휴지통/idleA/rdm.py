import random
from printer import printf

def rdm(t):
    c = random.choice
    cs = random.sample
    res = []
    if t == 0:
        fixPos = c(range(16))
        for i in range(2):
            m = ['0'] * 16
            m[fixPos] = 'x'
            for pack in '123456789abc':
                li = [j for j in range(16) if m[j] == '0']
                m[c(li)] = pack
            res.append(''.join(m))
        dire = c(range(8))
        res.append(dire)
    if t == 1:
        pass
    if t == 2:
        pass
    return res
