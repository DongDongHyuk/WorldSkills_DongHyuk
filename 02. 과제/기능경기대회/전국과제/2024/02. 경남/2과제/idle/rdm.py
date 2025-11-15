import random
from printer import printf
def rdm(t):
    res = []
    c = random.choice
    cs = random.sample
    if t == 0:
        hli = c([[26,29],[27,28]])
        xli = c([[18,35],[19,34]]) 
        xli += [{18 : 21, 19 : 20, 34 : 37, 35 : 36}[i] for i in xli]
        m = list('xxx00xxxxxxxxxxx0x0000x0xx0000xx0x0000x0xxxxxxxxxxx00xxx')
        m = ['x'  if i in xli else m[i] for i in range(56)]
        for pack in '112233445566':
            pos = c([i for i in range(56) if i not in hli + xli and m[i] == '0'])
            m[pos] = pack
        res.append(''.join(m)), res.append(hli)
    if t == 1:
        idxIn = [6,7,8,11,13,16,17,18]
        idxOut = [0,2,4,14,24,22,20,10]
        xli = [c(idxIn),c(idxOut)]
        resli = []
        di = {0:[2,10],2:[0,4],4:[2,14],14:[4,24],24:[14,22],22:[20,24],20:[10,22],10:[0,20]}
        used = xli[:]
        for _ in range(2):
            li = []
            for i in range(2):
                n = c([j for j in idxOut if j not in used and all([k not in li for k in di[j]])])
                li.append(n)
                used.append(n)
            resli.append(li)
        for i in range(2):
            m = list('0x0x0x000x00x00x000x0x0x0')
            m = ['x' if i in xli else m[i] for i in range(25)]
            for pack in '1234567':
                pos = c([i for i in idxIn if i not in used and m[i] == '0'])
                m[pos] = pack
            res.append(''.join(m))
        res.append(resli)
    if t == 2:
        for _ in range(2):
            m = list('0'*15)
            for i in range(3):
                pack = '123'[i]
                a,b = [(0,5),(6,9),(12,13)][i]
                pos = c([i for i in range(a,b)])
                m[pos] = pack
            for pack in '456789':
                pos = c([i for i in [0,1,2,3,4,6,7,8] if m[i] == '0'])
                m[pos] = pack
            res.append(''.join(m))
    return res