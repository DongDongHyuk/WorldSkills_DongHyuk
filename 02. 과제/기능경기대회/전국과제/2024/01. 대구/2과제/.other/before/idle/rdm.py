import random
from printer import printf
def rdm(t):
    res = []
    c = random.choice
    cs = random.sample
    if t == 0:
        for _ in range(2):
            m = ['0']*9
            pli = list('1234567')
            while pli:
                pos = c([i for i in range(9) if m[i] == '0' and (i < 3 or m[i - 3] not in '01')])
                pack = c(pli)
                pli.remove(pack)
                m[pos] = pack
            res.append(''.join(m))
    if t in [1,3]:
        for _ in range(2):
            m = ['0']*9
            for pack in '1234567':
                pos = c([i for i in range(9) if m[i] == '0'])
                m[pos] = pack
            res.append(''.join(m))
    if t == 2:
        for _ in range(2):
            pos = c(range(9))
            y,x = divmod(pos,3)
            axis = c('yx')
            line = [i for i in range(9) if (axis == 'y' and i // 3 == y) or (axis == 'x' and i % 3 == x)]
            m = ['0'] * 9
            m[pos] = '1'
            for pack in '234567':
                pos = c([i for i in range(9) if m[i] == '0' and i not in line])
                m[pos] = pack
            res.append(''.join(m))
        res.append(c(range(4)))
    return res
