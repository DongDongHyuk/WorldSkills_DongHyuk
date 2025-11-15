import random
from printer import printf

def aro(t,m):
    res = []
    if t == 0:
        for i in range(6):
            if m[i] == '0':
                if i < 2 or m[i-2] != '0':
                    res.append(i)
    if t == 3:
        for i in range(9*3):
            if m[i] == '0':
                if i >= 9:
                    if m[i-9] != '0':
                        res.append(i)
                else:
                    res.append(i)
    return res

def rdm(t):
    res = []
    c = random.choice
    if t == 0:
        m = ['0']*6
        for _ in range(5):
            pos,pack = c(aro(t,m)),c([i for i in '12345' if i not in m])
            m[pos] = pack
        res.append(''.join(m))
        res.append('142530')
    if t == 1:
        m = ['0']*14
        n = c([0,1,2,3,4,5])
        m[n],m[n+1] = 'b','b'
        for i in '1234':
            m[c([j for j in range(14)
                 if m[j] == '0' and (j < 7 or m[j-7] == 'b')])] = i
        res.append(''.join(m))
        res.append('1234bb0000000000')
    if t == 2:
        m = list('123456789')
        random.shuffle(m)
        res.append(''.join(m))
        res.append('123456789')
    if t == 3:
        n = c([0,1,2,3,4,5,6,7,8])
        for _ in range(2):
            m = ['0']*27
            for __ in range(14):
                pos = c(aro(t,m))
                packs = [i for i in '123456789abcde' if i not in m]
                m[pos] = c(packs)
            res.append(''.join(m))
    return res

rdm(2)
