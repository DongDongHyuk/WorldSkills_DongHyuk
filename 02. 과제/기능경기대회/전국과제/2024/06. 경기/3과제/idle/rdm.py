import random
from printer import printf
def rdm(t):
    c = random.choice
    cs = random.sample
    res = []
    if t < 2:
        for _ in range(2):
            m = [list('x0x0x00000x0x0x00000x0x0x'),list('x00x00000000x00x')][t]
            for pack in ['123456789abc','12345678'][t]:
                li = [i for i in [range(25),([1,2,4,5,6,7,8,9,10,11,13,14] if _ == 0 else [1,2,4,7,8,11,13,14])][t] if m[i] == '0']
                pos = c(li)
                m[pos] = pack
            res.append(''.join(m))
    if t == 2:
        m = list('12345678')
        random.shuffle(m)
        res.append(''.join(m))
    if t == 3:
        m = ['0'] * 8
        for pack in '123456':
            pos = c([i for i in range(6) if m[i] == '0'])
            m[pos] = pack
        res.append(''.join(m))
    return res