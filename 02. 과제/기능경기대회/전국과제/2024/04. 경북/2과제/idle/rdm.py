import random
from printer import printf
def rdm(t):
    c = random.choice
    cs = random.sample
    res = []
    if t == 0:
        m = list('0'*12)
        for st in ['123456','789abc']:
            li = cs(st,3)
            for pack in li:
                pos = c([i for i in range(6) if m[i] == '0'])
                m[pos] = pack
        li = [i for i in '123456789abc' if i not in m]
        for pack in li:
            pos = c([i for i in range(6,12) if m[i] == '0' and ((pack in '123456' and m[i-6] in '123456') or
                                                                (pack in '789abc' and m[i-6] in '789abc'))])
            m[pos] = pack
        res.append(''.join(m))
    if t == 1:
        m = list('123456000')
        random.shuffle(m)
        res.append(''.join(m))
    if t == 2:
        m = list('00000x000x00000')
        for li in [[0,1,6,11,10],[3,4,8,13,14]]:
            for _ in range(3):
                pos = c([i for i in li if m[i] == '0'])
                m[pos] = c([i for i in '123456' if i not in m])
        res.append(''.join(m))
        hli = [2,7,12]
        random.shuffle(hli)
        res.append(hli)
    if t == 3:
        pack = list('123456789abc')
        pack1 = cs(pack,6)
        pack2 = [i for i in pack if i not in pack1]
        for i in range(2):
            m = ['0'] * 9
            pack = pack2 if i else pack1
            for pack in pack:
                pos = c([i for i in range(9) if m[i] == '0'])
                m[pos] = pack          
            res.append(''.join(m))

    return res
