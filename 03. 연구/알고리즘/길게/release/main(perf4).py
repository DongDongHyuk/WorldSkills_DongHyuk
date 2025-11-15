from time import time
from Tool.Printer import *
from queue import PriorityQueue
from collections import deque

def exc(m,s,e,r):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    info = [r,int(m[s])]
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

def exp(n,m,p=-1):
    res = []
    di1,di2 = {},{}
    for i in range(si):
        if not fx[i] and m[i] != 'x':
            if m[i] != '0':
                di1[i] = i
            if m[i] == '0' or n < 1:
                di2[i] = i
    if n < 1:
        return [[i,i] for i in aro(p) if i in di2]
    for i in di1 if n > 0 else [p]:
        q = [i]
        r = {i:[di1[i]]}
        for cur in q:
            for j in aro(cur):
                if j in q or j not in di2:
                    continue
                q.append(j)
                r[j] = r[cur] + [di2[j]]
                if j not in hli:
                    res.append(exc(m,di2[j],di1[i],r[j]))
    return res

visited = 0
def src(n,m,*a):
    global res
    global visited       # temp
    if n < 1:
        s,e = a
        if n == 0 and (n,s,e) in cache:
            return cache[n,s,e]
    if n == 1:
        leaf,p,pk = a    
    cur = m if n > 0 else s
    q = PriorityQueue() if n > 0 else deque([])
    mkd = {cur:[cur]}
    g = {cur:0}    
    def heu0(m):
        ct = 0
        if p != -1:
            rp = len([i for i in src(0,m,m.index(pk),p) if m[i] not in '0'+pk])
            ct += 10000 * rp
            r2 = src(-1,m,p,-1)
            isDead = len(r2) > 1
        for i in range(si):
            if m[i] not in '0x':
                y1,x1 = divmod(i,sx)
                y2,x2 = divmod(p if p!=-1 else leaf.index(m[i]),sx)
                dst = (abs(y1 - y2) + abs(x1 - x2)) + 1
                ct += (100 * (si - dst) if isDead and i in r2 else -dst) if p != -1 else dst ** 2
        if p != -1 and not rp:
            ct = -2 ** (30 if m[p] == pk else 20)
        return ct
    put = lambda cur: q.put((g[cur] + heu0(cur), cur)) if n > 0 else q.append(cur)
    get = lambda : q.get()[1] if n > 0 else q.popleft()
    put(cur)
    while 1:
        if n == -1 and len(q) > 1:      # default
            break
        cur = get()
        if n > 0:      # temp
            visited += 1
        if n == -2 and m[cur] != '0' and cur not in e:
            break
        if n == 0 and cur == e:
            break
        if n == 1:
            if (p == -1 and cur == leaf) or (p != -1 and cur[p] == pk):
                break
        for i,j in exp(n,cur if n > 0 else m,cur):
            if i not in mkd:
                mkd[i] = mkd[cur] + [j]
                g[i] = g[cur] + 1
                put(i)
    res1 = mkd[cur]
    if n > 0:
        res += res1[1:]
        return cur
    if n == 0:
        cache[n,s,e] = res1
    return res1

def main(g_t,m,*a):
    global t,sy,sx,si,fx,fxli,cache,res
    t = g_t
    sy,sx = [[None,None],[None,None],[None,None]][t]
    si = sy * sx
    fx = {i:0 for i in range(si)}
    fxli = lambda li,n: fx.update({i:n for i in li})
    cache = {}
    res = []
    if t == 0:
        global hli
        leaf,hli = a
    seq = []
    hd,hdr = [],{}
    leaf1 = list(leaf[:])
    for i in seq:
        pk = leaf1[i]
        if pk == '0':
            r = src(-2,leaf1,i,hd)
            pk = leaf1[r[-1]]
            hd.append(i)
            hdr[i] = r
            leaf1[r[-1]],leaf1[i] = '0',pk
        m = src(1,m,''.join(leaf1),i,pk)
        fx[i] = 1
    m = src(1,m,''.join(leaf1),-1,-1)
    for i in hd[::-1]:
        res.append([hdr[i],int(m[i])])
    return res

if __name__ == '__main__':
    t,m1,m2 = 0,None,None
    ts = time()
    res = main(t,m1,m2,hli) if t == 0 else main(t,m)
    te = time() - ts
    print(res)
    print('visited :',visited)
    print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))

