from collections import deque
from functools import lru_cache

from time import time
from printer import printf
from rdm import rdm

def exc(m,s,e):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    return [''.join(m),[e,s]]

@lru_cache(maxsize=None)
def aro(t,pos):
    res = []
    dy,dx = [-1,0,1,0]*5,[0,1,0,-1]*5
    dz = [-2,-2,-2,-2,-1,-1,-1,-1,0,0,0,0,1,1,1,1,2,2,2,2]
    y,x,z = (pos // sx) % sx, pos % sx, pos // size
    for i in range(20):
        ny,nx,nz = y + dy[i],x + dx[i],z + dz[i]
        if -1 < ny < sy and -1 < nx < sx and -1 < nz < sz:
            n = ny * sx + nx + (size * nz)
            res.append(n)
    return res

def exp(n,m,pos=None):
    res = []
    for i in range(size*sz) if n else [pos]:
        if (n and m[i] != '0') or i in fix:
            continue
        for j in [j for j in aro(t,i)
                  if m[j] not in ['x','0x'][n] and j not in fix]:
            if t == 0 and n and \
                ((i >= size and m[i - size] == '0') or 
                (j < size*(sz-1) and m[j + size] != '0')):
                    continue
            res.append(exc(m,i,j) if n else [j,j])
    return res
    
def bfs(n:'0 : 길찾기, 1 : 정렬',m,*a):
    global res
    if n:
        leaf,pos,pack = a
    else:
        s,e = a        
    cur = m if n else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n:
            if cur == leaf or \
                (pos != -1 and cur[pos] == pack):
                    break
        elif cur == e:
            break
        for i,j in exp(n,cur if n else m,cur):
            if i not in mkd:
                que.append(i)
                mkd[i],step[i] = cur,j
    mkd[-2] = cur 	
    path = [step[cur]]
    while mkd[cur] != -1:
        cur = mkd[cur]
        path.append(step[cur])
    if n:
        res += path[::-1][1:]
        return mkd[-2]
    return path[::-1][1:]
    
def sort(m,leaf,e):
    pack = leaf[e]
    res = []
    s = m.index(pack)
    road = [s]+bfs(0,m,s,e)
    for i in range(len(road)):
        n = road[i]
        if t == 0 and n < 16:
            if i:
                fix.append(road[i-1])
                fix.append(road[i-1]+9)
            m = bfs(1,m,leaf,n+9,'0')
            if i:
                del fix[-2:]
        
        m = bfs(1,m,leaf,n,pack)
    fix.append(e)
    return m

def main(g_t,y,x,z,m,*a):    
    global t,sy,sx,sz,size,fix,res
    t = g_t
    sy,sx,sz = y,x,z
    size = sy * sx
    fix = []
    res = []    
    if t == 0:
        global h
        h, = a
        h = [h+9,h+18]
        
        '''
        층 제한 구현
        고정하면 안되고 지나갈 수는 있게 만들어야됨
        -> exp 수정 : m의 h에 팩이 있으면 무조건 옮김
            
        '''
        
        for i in list(range(size*(sz-1))):
            if leaf[i] != '0':
                ts = time()                
                m = sort(m,leaf,i)      # short bfs                
                te = time() - ts

                
        m = bfs(1,m,leaf,-1,-1)         # default bfs        
    return res

h,root,leaf = 2,'30d59eca000071b860000004200','5d7b604e03208a00009c0100000'
print("h,root,leaf = {},'{}','{}'".format(h,root,leaf))
ts = time()
res = main(0,3,3,3,root,h)
te = time() - ts
print(res)
print(len(res),'step','{}s'.format(round(te,3)))



