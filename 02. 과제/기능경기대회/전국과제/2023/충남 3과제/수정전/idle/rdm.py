import random
from printer import printf
def rdm(t):
    c = random.choice
    cs = random.sample
    if t == 0:
        pass
    if t == 1:
        m = ['0'] * 16
        li = list('123'+c('123'))
        for i in range(6):
            if i == 4:
                li = [j for j in '123' if m.count(j) < 2]
            def get_pos(m):
                li = []
                for x in range(4):
                    for z in range(4):
                        pos = 4 * z + x
                        if m[pos] == '0':
                            li.append(pos)
                            break
                return li
            res0 = get_pos(m)
            li1 = [j for j in res0 if j < 4]
            pos = li1[0] if li1 else c(res0)
            pack = c(li)
            li.remove(pack)
            m[pos] = pack
        li = [2,2,3,3]
        random.shuffle(li)

        ct = [0,0,0]        # 팩별 가져와야하는 팩 갯수
        for i in range(4): 
            pack = m[i]
            ct[int(pack)-1] += li[i]
        for i in range(3):
            ct[i] -= m.count(str(i+1))

        li1 = get_pos(m)        # 열 마다 제일 높은곳
        li2 = []        # 가져올 팩 순서
        for i in range(3):
            li2 += [i+1] * ct[i]
        for i in range(4):
            m[li1[i]] = str(li2[i])
        
        res = [''.join(m),li]
    if t == 2:
        m = ['0'] * 8
        m[c(range(8))] = 'x'
        for i in '112233':
            pos = c([i for i in range(8) if m[i] == '0'])
            m[pos] = i
        res = ''.join(m)
    return res
