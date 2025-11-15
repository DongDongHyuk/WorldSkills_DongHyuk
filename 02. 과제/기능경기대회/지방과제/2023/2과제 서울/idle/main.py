from collections import deque
from printer import *

def exc(m,s,e):
    m = list(m)
    m[s],m[e] = m[e],'0'
    return ''.join(m)
    
def exp(mode,m,pos = None):
    res = []
    dxy = [-5,1,5,-1]
    wall = [[0,1,2,3,4],[4,9,14,19,24],[20,21,22,23,24],[0,5,10,15,20]]
    li = [i for i in range(25) if m[i] == '0' and i not in fix] if mode else [pos]
    for pos in li:
        for i in range(4):
            npos = pos + dxy[i]
            if pos not in wall[i] and \
                m[npos] not in ['9','0' if mode else None] and npos not in fix:
                    res.append(exc(m,pos,npos) if mode else npos)
    return res
    
def bfs(mode,m,*n):
    if not mode:
        s,e = n
    else:
        li,pos,pack = n
    cur = m if mode else s
    que = deque([cur])
    mkd = {cur:'s'}
    while 1:
        cur = que.popleft()
        if not mode and cur == e:
            break
        if mode:
            if not any([int(cur[i]) for i in li]) and \
                (None in [pos,pack] or cur[pos] == pack):
                    break
        for i in exp(mode,cur if mode else m,cur):
            if i not in mkd:
                mkd[i] = cur
                que.append(i)
    mkd['e'] = cur
    return (mkd,cur) if mode else mkd
    
def path(mkd):
    cur = mkd['e']
    path = [cur]
    while mkd[cur] != 's':
        cur = mkd[cur]
        path.append(cur)
    return path[::-1][1:]
    
def con(res):
    path = []
    fir = res[0]
    for sec in res[1:]:
        step = [None] * 2
        for i in range(25):
            if fir[i] != sec[i]:
                if fir[i] == '0':
                    step[1] = i
                else:
                    step[0] = i
        path.append(step)
        fir = sec[:]
    return path
    
def main(mode,m,*n):
    global fix
    fix = []
    m = ''.join(m)
    if not mode:
        s,e = n
        res = [s]
        res += path(bfs(0,m,s,e))
        return res
    else:
        li,pos,pack = n
        res = [m]
        iss = False
        if li:
            for i in li:
                if m[i] != '0':
                    res0 = exp(0,m,i)
                    if res0 == [pos]:
                        iss = True
                    if len(res0) == 2 and pos in res0 and \
                        exp(0,m,[j for j in res0 if j != pos][0]) == [i]:
                            iss = True
        if not iss:
            fix.append(pos)
            li.remove(pos)
        for i in range(1,len(li)+1):
            mkd,m = bfs(1,m,li[0:i],None,None)
            res += path(mkd)
        if iss and m[pos] != pack:
            e = pos
            pli = [i for i in range(25) if m[i] == pack]
            def dist(s,e):
                s,e = map(lambda n: divmod(n,5),[s,e])
                return abs(s[0] - e[0]) + abs(s[1] - e[1])
            s = min(pli,key = lambda n: dist(n,e))
            r = main(0,m,s,e)
            for i in r:
                mkd,m = bfs(1,m,[j for j in li if i != j],i,pack)
                res += path(mkd)
        return con(res),list(m)

import time
ts = time.time()
main(1,'9309232003029190011000000',[4,9,8,7,2,1],9,'3')
te = time.time() - ts
print(te)
