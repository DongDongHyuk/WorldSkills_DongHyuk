from collections import deque
from printer import *
import time

def exc(m,s,e):
    m = list(m)
    m[s],m[e] = m[e],'0'
    return ''.join(m)

def exp(mode,m,pos = None):
    res = []
    dxy = [-5,1,5,-1]
    wall = [[0,1,2,3,4],[4,9,14,19,24],[20,21,22,23,24],[0,5,10,15,20]]
    li = [i for i in range(len(m)) if m[i] == '0' and i not in fix] if mode else [pos]
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
        li,fp = n
    cur = m if mode else s
    que = deque([cur])
    mkd = {cur:'s'}
    while 1:
        cur = que.popleft()
        if not mode and cur == e:
            break
        if mode == 1:
            if not any([int(cur[i]) for i in li]) and \
               (not fp or cur[fp[0]] == fp[1]):
                    break               
        for  i in exp(mode,cur if mode else m,cur):
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
        for i in range(len(sec)):
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
        li,fp = n
        res = [m]
        iss = False
        if li:
            for i in [li[-1],li[0]]:
                if m[i] != '0' and [fp[0]] == exp(0,m,i):
                    iss = True
        if not iss:
            fix.append(fp[0])
        for i in range(1,len(li)+1):
            mkd,m = bfs(1,m,li[0:i],None)
            res += path(mkd)
        if iss and m[fp[0]] != fp[1]:
            e = fp[0]
            pli = [j for j in range(len(m)) if m[j] == fp[1]]
            def dist(s,e):
                s,e = map(lambda pos: divmod(pos,5),[s,e])
                return abs(s[0] - e[0]) + abs(s[1] - e[1])
            s = min(pli,key = lambda pos: dist(pos,e))
            r = main(0,m,s,e)
            for i in r:
                mkd,m = bfs(1,m,[j for j in li if j != i],[i,fp[1]])
                res += path(mkd)
        return con(res),list(m)

ts = time.time()

main(1,'0000000000193903022119392',[20,16,17,18,19,24],[15,'3'])

te = (time.time() - ts)
m,s = int(te // 60), round(te % 60,3)
print(m,'분',s,'초')
