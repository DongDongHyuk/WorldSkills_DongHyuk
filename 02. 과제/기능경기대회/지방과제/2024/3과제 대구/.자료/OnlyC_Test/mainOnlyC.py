from collections import deque
from printer import printf
from time import time

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    step = [e,s] if li == -1 else li
    info = []
    for i in li:
        pack = 'abc'.index(i[1])+10 if i[1].isalpha() else int(i[1])
        info.append([i[0],pack])
        for j in i[0]:
            m[j] = '0'
    for i in li:
        li1,pack = i[0],i[1]
        m[li1[1]] = pack
    return [''.join(m),info]
def exp(n,m,pos=-1):
    res = []
    for i in range(10) if n > 0 else [pos]:
        ct = 1+i
        ct_ = 0
        for j in range(9-i):
            res1 = []
            for k in range(ct):
                for l in range(0,20,10):
                    if m[j+k+l] != '0':
                        pos1 = j+k+l
                    if m[ct-k+j+l] != '0':
                            pos2 = ct-k+j+l
                if pos1 in fix or pos2 in fix:
                    ct_ = 1
                    continue
                pos3,pos4 = pos2,pos1
                if (pos1 < 10 and pos2 < 10) or (pos1 > 9 and pos2 > 9):
                    pos3 = pos2+10 if pos1 < 10 else pos2-10
                    pos4 = pos1+10 if pos1 < 10 else pos1-10
                if pos1 == pos2:
                    res1.append([[pos1,pos3],m[pos1]])
                    break
                else:
                    res1.append([[pos1,pos3],m[pos1]])
                    res1.append([[pos2,pos4],m[pos2]])
                    if (ct == 3 and k == 1) or (ct == 5 and k == 2) or \
                        (ct == 7 and k == 3) or (ct == 9 and k == 4) or ct == 1:
                        break
            if ct_ != 0:
                ct_ = 0
                continue
            res.append(exc(m,-1,-1,res1))
        if i == 9:
            return res
        continue
    return res
def bfs(n,m,*a):
    global res
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 3:
        pack,li = a
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n == 0 and cur == e:
            break
        if n == 1:
            if (pos == -1 and cur == leaf) or \
               (pos != -1 and cur[pos] == pack):
                break
        if n == 3:
            if ''.join([cur[i] for i in li]) == pack:
                break
        for i,j in exp(n,cur if n > 0 else m,cur):
            if i not in mkd:
                que.append(i)
                mkd[i],step[i] = cur,j
    mkd[-2] = cur
    path = [step[cur]]
    while mkd[cur] != -1:
        cur = mkd[cur]
        path.append(step[cur])
    if n > 0:
        res += path[::-1][1:]
        return mkd[-2]
    return path[::-1][1:]
def main(g_t,m,*a):    
    global t,fix,res,cache
    t = g_t
    fix = []
    res = []
    cache = {}      # cache reset
    leaf, = a
    for i in range(5):
        for j in range(0,20,10):
            if leaf[i+j] != '0' and leaf[i+j] != m[i+j]:
                m = bfs(1,m,leaf,i+j,leaf[i+j])
        pos = i+j-10 if i+j > 9 else i+j+10
        fix += [i+j,pos]
    li = []
    pack = []
    for i in range(5,10):
        for j in range(0,20,10):
            if leaf[i+j] != '0':
                li.append(i+j)
                pack.append(leaf[i+j])
    pack = ''.join(pack)
    for i in range(1,len(li)+1):
        m = bfs(3,m,pack[:i],li[:i])
    res1 = []
    for i in res:
        res1 += i
    res = res1
    return res


# t,root,leaf = 2,'8006a503470920001000','28a01900000005003746'       # FirstCaseC
t,root,leaf = 2,'30070609a10480502000','0000023000485790061a'       # SecondCaseC

ts = time()    
res = main(t,root,leaf)    
te = time() - ts
print(res)
print("{}step, idle {}s(dart {}m {}s) \n".
format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))