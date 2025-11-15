from collections import deque
from time import time
from printer import printf

def exc(m,s,e):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    info = [[e,s],int(m[s])]
    return [''.join(m),info]
    
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
    for i in range(size) if n > 0 else [pos]:       
        if (n > 0 and m[i] != '0') or i in fix:
            continue        
        for j in [j for j in aro(i) if m[j] not in ['x','0x'][n > 0] and j not in fix]:            
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def bfs(n,m,*a):
    global res
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n == 0 and cur == e:
            break
        if n == 1:
            if (pos == -1 and cur == leaf) or (pos != -1 and cur[pos] == pack):
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
    
def sort(m,leaf,pos,pack):
    r = bfs(0,m,m.index(pack),pos)
    for i in r:
        m = bfs(1,m,leaf,i,pack)
    fix.append(pos)
    return m

def main(g_t,m,*a):    
    global t,sy,sx,size,fix,res,cache
    t = g_t
    sy,sx = [[0,0],[0,0],[0,0]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}      # cache reset
    if t == 0:
        pass
    return res

if __name__ == '__main__':

    t,m,leaf = 0,'',''
        
    ts = time()    
    res = main(t,m,leaf)    
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
