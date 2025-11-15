import random
from printer import printf
def rdm(t):
    c = random.choice
    rdp = lambda m: c([i for i in range(len(m)) if m[i] is '0'])
    if t == 0:
        pack = ['1','2','3']
        m = '0'*16
        m = list(m)
        while 1:
            if not pack:
                hold = [i for i in range(16) if m[i] != '0']
                if [i for i in [[1,4],[2,7]] if hold[:-1] == i] or\
                   [i for i in [[8,13],[11,14]] if hold[1:] == i] or\
                   [i for i in [[2,5,8],[1,6,11],[4,9,14],[7,10,13]] if hold == i]:
                    pack = ['1','2','3']
                    m = '0'*16
                    m = list(m)
                    continue
                else:
                    break
            res1 = []
            a = rdp(m)
            y,x = divmod(a,4)
            dy = [-1,-2,-3,1,2,3,0,0,0,0,0,0]
            dx = [0,0,0,0,0,0,-1,-2,-3,1,2,3]
            for i in range(12):
                ny,nx = y + dy[i],x + dx[i]
                if -1 < ny < 4 and -1 < nx < 4:
                    res1.append(ny * 4 + nx)
            if len([i for i in res1 if m[i] =='0']) == 6:
                m[a] = pack[0]
                pack.remove(pack[0])
        # 고정팩 갇히는 조건 넣어주기
        hold = [i for i in range(16) if m[i] != '0']
        pack = '112233'
        pack = list(pack)
        while pack:
            a = rdp(m)
            b = c(pack)
            m[a] = b
            pack.remove(b)
        res = ''.join(m),hold
    if t == 1:
        m = 'x000x0000000000x000x'
        m = list(m)
        m[c([5,10])],m[c([9,14])] = 'x','x'
        li = [1,2,3,16,17,18]
        for i in range(3):
            a = c(li)
            m[a] = 'x'
            li.remove(a)
        leaf = m[:]
        pack = '123456'
        pack = list(pack)
        li = [6,7,8,11,12,13]
        for i in range(6):
            a = c(li)
            b = c(pack)
            m[a] = b
            li.remove(a)
            pack.remove(b)
        for i in range(1,7):
            a = [0,6,7,8,11,12,13][i]
            leaf[a] = '0123456'[i]
        inx = '0'*8
        inx = list(inx)
        pack = '123456'
        pack = list(pack)
        for i in range(6):
            a = rdp(inx)
            b = c(pack)
            inx[a] = b
            pack.remove(b)
        inx = list(map(int,inx))
        res = ''.join(m)
    if t == 2:
        m = '0'*25
        m = list(m)
        hole = []
        while len(hole) != 2:
            a = rdp(m)
            if a not in hole:
                hole.append(a)
        li = [i for i in range(25) if i%2 != 0]
        li1 = [i for i in range(25) if i not in li]
        while 1:
            a = c(li)
            if a in hole:
                continue
            if len(li) == 10:
                break
            m[a] = '7' if len(li) == 12 else '8'
            li.remove(a)
        while 1:
            a = c(li1)
            if a in hole:
                continue
            if len(li1) == 11:
                break
            m[a] = '5' if len(li1) == 13 else '6'
            li1.remove(a)
        pack = '1234'
        pack = list(pack)
        while pack:
            a = rdp(m)
            if a not in hole:
                b = c(pack)
                m[a] = b
                pack.remove(b)
        leaf = list('0'*25)
        li = [i for i in range(25) if i%2 != 0]
        li1 = [i for i in range(25) if i not in li]
        while 1:
            a = c(li)
            if a in hole:
                continue
            if len(li) == 10:
                break
            leaf[a] = '7' if len(li) == 12 else '8'
            li.remove(a)
        while 1:
            a = c(li1)
            if a in hole:
                continue
            if len(li1) == 11:
                break
            leaf[a] = '5' if len(li1) == 13 else '6'
            li1.remove(a)
        pack = '1234'
        pack = list(pack)
        while pack:
            a = rdp(leaf)
            if a not in hole:
                b = c(pack)
                leaf[a] = b
                pack.remove(b)
        res = [''.join(m),''.join(leaf),hole]
    return res

print(rdm(1))
