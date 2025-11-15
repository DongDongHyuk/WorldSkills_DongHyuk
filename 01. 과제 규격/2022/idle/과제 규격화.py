from collections import deque

from time import time
from rdm import rdm
from printer import printf

def exc(m,s,e):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    return [''.join(m),[e,s]]

cache = {}      # cache
def aro(pos):
    if pos in cache:
        return cache[pos]
    res = []
    dy,dx = [-1,0,1,0],[0,1,0,-1]
    y,x = divmod(pos,sx)
    for i in range(4):
        ny,nx = y + dy[i],x + dx[i]
        if -1 < ny < sy and -1 < nx < sx:
            res.append(ny * sx + nx)
    cache[pos] = res
    return res   

def exp(n,m,pos=-1):
    res = []
    for i in range(size) if n else [pos]:       
        if (n and m[i] != '0') or i in fix:
            continue        
        for j in [j for j in aro(i)
                  if m[j] not in ['x','0x'][n] and j not in fix]:            
            res.append(exc(m,i,j) if n else [j,j])
    return res
    
def bfs(n,m,*a):
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
    r = bfs(0,m,s,e)
    for i in r:
        m = bfs(1,m,leaf,i,pack)
    return m

def main(g_t,m,*a):
    global t,sy,sx,size,fix,res
    t = g_t
    sy,sx = [[4,4]][t]
    size = sy * sx
    fix = []
    res = []
    if t == 0:
        leaf, = a
        li = [0,15,3,12,1,7,14,8,2,11,13,4,5,6,9,10]
        for i in li:
            if leaf[i] != '0':
                m = sort(m,leaf,i)
                fix.append(i)
    return res

if __name__ == '__main__':
    
    Type,root,leaf= 0,'0b89672300c0514a','123456789abc0000'

    ts = time()    
    res = main(Type,root,leaf)    
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))

