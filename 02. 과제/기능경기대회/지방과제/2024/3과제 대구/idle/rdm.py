import random
from printer import printf

def rdm(t):
    res = []
    c = random.choice
    if t == 0:
        pass
    if t == 1:
        for i in range(2):
            m = ['0'] * 12
            for j in range(9):
                li1 = [k for k in range(12) if (k < 3 or m[k - 3] != '0') and m[k] == '0']
                li2 = [k for k in '123456789' if k not in m]
                pos,pack = c(li1),c(li2)
                m[pos] = pack
            res.append(''.join(m))
        res.append(c('123456789'))
    if t == 2:
        for i in range(2):
            m = ['0'] * 20
            for j in range(10):
                li1 = [k for k in range(20) if m[k] == '0' and ((k < 10 and m[k + 10] == '0') or (k > 9 and m[k - 10] == '0'))]
                li2 = [k for k in '123456789a' if k not in m]
                pos,pack = c(li1),c(li2)
                m[pos] = pack
            res.append(''.join(m))
    return res
