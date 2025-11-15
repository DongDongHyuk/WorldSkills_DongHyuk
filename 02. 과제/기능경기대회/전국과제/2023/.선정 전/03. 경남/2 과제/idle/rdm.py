import random
from printer import printf

def rdm(t):
    c = random.choice
    cs = random.sample
    if t == 0:
        res = []
        hli = [[],[]]
        for i in range(2):
            for j in range(3):
                pos = c([k for k in range(5*j,5*(j+1)) if not (i and k in hli[0])])
                hli[i].append(pos)
        pack_count = [-1,0,0,0,0,0,0]
        for i in range(2):
            m = ['0'] * 15
            for _ in range(9):
                pack = c([j for j in [1,2,3,4,5,6] if pack_count[j] < 3])
                pack_count[pack] += 1
                pos = c([j for j in range(15) if j not in hli[i] and m[j] == '0'])
                m[pos] = str(pack)
            res.append(''.join(m))
        res.append(hli)
    if t == 1:
        res = []
        hli = cs([i for i in range(20)],3)
        for i in range(2):
            m = ['0'] * 20
            for pack in '123456789abc':
                pos = c([j for j in range(20) if j not in hli and m[j] == '0'])
                m[pos] = pack
            res.append(''.join(m))
        res.append(hli)
    if t == 2:
        res = []
        li = cs(list(range(1,7)),3)
        hli = [cs(list(range(12)),3),li[:],li[:]]
        for i in range(2):
            m = ['0'] * 12
            for pack in '123456':
                pos = c([j for j in range(12) if j not in hli[0] and m[j] == '0'])
                m[pos] = pack
            res.append(''.join(m))
            random.shuffle(hli[i+1])
        res.append(hli)
    return res

print(rdm(2))
