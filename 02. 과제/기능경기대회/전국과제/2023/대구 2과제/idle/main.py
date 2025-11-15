from collections import deque
from time import time
from printer import printf

def exc(m,s,e,li,g=-1,p=-1):
    m = list(m)
    li = list(li) if t < 3 else -1
    con = lambda n: ord(n)-87 if ord(n) > 96 else int(n)
    if g != -1:
        m[s] = '0' if g else p
        li.append(p) if g else li.remove(p)
        return [(''.join(m),tuple(li)),[s,g,con(p),e]]
    m[s],m[e] = m[e],m[s]
    if t == 1 and m[s] == 'b':
        step = [e,s]
        m[e],m[e+(e-s)] = 'b','0'
        n = [i+sx for i in range(sx) if m[i+sx] != '0']
        if n:
            n, = n
            n1,n2 = n+(s-e),n
            m[n1],m[n2] = m[n2],'0'
        if m[s+sx] != '0':
            step = [e+(e-s),e]
        step.append(m.index('b'))
        step += [n2,n1,con(m[n1])] if n else [-1]*3
    else:
        if t == 2:
            li=[-1,1] if li==[-3,3] else [-3,3]
            step = [e,s,con(m[e]),con(m[s])]
        else:
            step = [e,s,con(m[s])]
    return [(''.join(m),tuple(li)) if t < 3 else ''.join(m),step]

def aro(pos):
    if pos in cache:
        return cache[pos]
    res = []
    dy,dx = [[0,0,0,0]*5,[-3,-1,1,3]*5] if t == 1 else [[-1,0,1,0]*5,[0,1,0,-1]*5]
    dz = [-2,-2,-2,-2,-1,-1,-1,-1,0,0,0,0,1,1,1,1,2,2,2,2]
    y,x,z = (pos // sx) % sy, pos % sx, pos // size
    for i in range(20):
        ny,nx,nz = y + dy[i],x + dx[i],z + dz[i]
        if -1 < ny < sy and -1 < nx < sx and -1 < nz < sz:
            n = ny * sx + nx + (size * nz)
            res.append(n)
    cache[pos] = res
    return res

def exp(n,m,pos=-1):
    res = []
    if t < 3:
        m,li = m
    for i in range(size*sz) if n else [pos]:        
        if t == 0 and m[i] != '0' and len(li) < 2 and (i > 3 or m[i+2] == '0'):            
                res.append(exc(m,i,-1,li,1,m[i]))
        if t == 0 and m[i] == '0' and li and (i > 3 or m[i+2] == '0') and (i < 2 or m[i-2] != '0'):
            for j in li:
                res.append(exc(m,i,-1,li,0,j))                
        if ((n and m[i] != '0') and t not in [1,2]) or i in fix:
            continue        
        for j in [j for j in aro(i) if m[j] not in ['x','0x'][n > 0] and j not in fix]:
            if t == 0 and len(li) == 2:
                continue            
            if t == 0 or (t == 3 and n):
                if (i >= size and m[i - size] == '0') or (j < size*(sz-1) and m[j + size] != '0'):
                        continue
            if t == 1:
                d = abs(i-j)
                if d == 1 and m[j] == 'b' and m[i] not in '0b' and len(li) < 1:
                    res.append(exc(m,i,-1,li,1,m[i]))                    
                if m[i] != '0':
                    continue
                if d == 1 and m[j] == 'b' and m[j+sx] == '0' and li:
                    for k in li:
                        res.append(exc(m,i,j,li,0,k))             
                b1 = (m[j] in '135' and any([k in '135' for k in li])) or \
                     (m[j] in '246' and any([k in '246' for k in li]))
                b2 = d in [sx-3,sx+3]
                b3 = m[j] == 'b' and m[sx:].count('0') < sx-1
                b4 = d == 3 and (m[j] == 'b' or m[i+((j-i)//3)] != 'b' or m[sx:].count('0') < sx)
                b5 = i >= sx and (m[i - sx] != 'b' or m[j] == 'b')
                if any([b1,b2,b3,b4,b5]):
                    continue
            if t == 2 and i-j not in li:
                continue                        
            res.append(exc(m,i,j,li if t < 3 else -1) if n else [j,j])            
    return res

def bfs(n,m,*a):
    global res
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 2:
        li, = a
    cur = m if n else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n == 0 and cur == e:
            break
        if n == 1:
            cur1,li = cur if t < 3 else (cur,-1)
            if cur1 == leaf or \
               (pos != -1 and cur1[pos] == pack and (t != 1 or not li)):
                    break
        if n == 2 and all([cur[i] == '0' for i in li]):
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
    s = m.index(pack)
    road = [s]+bfs(0,m,s,e)
    for i in range(len(road)):
        n = road[i]
        if t == 3 and n < 18:            
            if i:
                fix.append(road[i-1])
                fix.append(road[i-1]+9)
            li = [j for j in range(n,27,9) if j != s][::-1]
            for j in range(4):
                m = bfs(2,m,li[:j])
            if i:
                del fix[-2:]
        m = bfs(1,m,leaf,n,pack)    
    fix.append(e)
    return m

def main(g_t,m,*a):    
    global t,sy,sx,sz,size,fix,res,cache
    t = g_t
    sy,sx,sz = [[1,2,3],[1,7,2],[3,3,1],[3,3,3]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}
    if t == 0:
        m,leaf = (m,()),'142530'
        bfs(1,m,leaf,-1,-1)
    if t == 1:
        m,leaf = (m,()),'1234bb00000000'
        for i in range(7):
            m = bfs(1,m,leaf,i,leaf[i])
            fix.append(i)
    if t == 2:
        m,leaf = (m,(-1,1)),'123456789'
        for i in range(3):
            m = bfs(1,m,leaf,i,leaf[i])
            fix.append(i)
        bfs(1,m,leaf,-1,-1)
    if t == 3:
        leaf, = a
        for i in range(18):
            if leaf[i] != '0':
                m = sort(m,leaf,i)
        for i in range(3):
            for j in range(i,27,9):
                if j not in fix:
                    m = bfs(1,m,leaf,j,leaf[j])
                    fix.append(j)
        bfs(1,m,leaf,-1,-1)
    return res

if __name__ == '__main__':

    # IDLE
    t,m1 = 0,'415320'
    t,m1 = 1,'2403bb10000000'
    t,m1 = 2,'671348952'
    t,m1,m2 = 3,'2e413896c05007d00a0b0000000','003ca102e00007b0590000840d6'

    # DART
    t,m1 = 0,'415320'
    t,m1 = 1,'bb304002100000'
    t,m1 = 2,'671348952'
    t,m1,m2 = 3,'30d59eca000071b860000004200','5d7b604e03208a00009c0100000'

    ts = time()
    if t == 3:
        res = main(t,m1,m2)
    else:
        res = main(t,m1)
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
    
