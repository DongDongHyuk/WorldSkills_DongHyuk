import random
from printer import printf
from main import exc
def rdm(t):
    res = []
    c = random.choice
    rdp = lambda m,li=-1: c([i for i in (range(len(m)) if li is -1 else li) if m[i] is '0'])
    if t == 0:
        pass
    if t == 1:
        for i in range(2):
            m1 = list('0' * (4*3))
            for j in '123456789':
                pos = rdp(m1)
                m1[pos] = j
            li = []
            li1 = []
            for j in range(12):
                for x in range(3):
                    for z in range(4):
                        pos = 3 * z + x
                        if m1[pos] == '0':#0이랑 같은것
                            li.append(pos)
                            for l in li:
                                if l not in [0,1,2]:
                                    if m1[l - 3] != '0':
                                        li1 = list(exc(m1,l,l-3)[0])
                                        m1 = li1
                                        
            res.append(''.join(m1[::-1]))
            a = []
            if len(res) == 2:
                pack = [k for k in '123456789']
                a = c(pack)
                res.append(a)
        
    if t == 2:
        pass
    return res
rdm(1)
