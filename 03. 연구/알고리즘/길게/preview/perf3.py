from time import time
from Tool.Printer import *
from queue import *

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
    for i in range(size) if n > 0 else [p]:
        if fx[i] or m[i] == 'x' or (n > 0 and m[i] == '0'):
            continue
        di = src(-1,m,i,-1) if n > 0 else aro(i)
        for j in di:
            if j == i or fx[j] or m[j] == 'x' or (n == -1 and m[j] != '0'):
                continue
            res.append(exc(m,j,i,di[j]) if n > 0 else [j,j])        
    return res

def src(n,m,*a):
    global res
    if n < 1:
        s,e = a
        if (n,s,e) in cache:
            return cache[(n,s,e)]
    if n == 1:
        leaf,p,pk = a
    cur = m if n > 0 else s
    q = PriorityQueue() if n > 0 else []
    mkd = {cur:[cur]}
    g = {cur:0}
    def heu(m):
        ct = 0
        for i in range(size):
            if m[i] not in '0x'+('' if p == -1 else pk):
                y1,x1 = divmod(i,sx)
                y2,x2 = divmod(leaf.index(m[i]) if p == -1 else p,sx)
                ct += (abs(y1 - y2) + abs(x1 - x2)) * (1 if p == -1 else -1)
        if p != -1:
            r1 = src(-2,m,p,-1)
            isDead = len(r1) > 1
            if isDead:
                for i in range(len(r1)-1,-1,-1):
                    if m[r1[i]] not in '0' + ('' if i else pk):
                        ct += 10 * (len(r1) - i if isDead else 1)
            r2 = src(0,m,m.index(pk),leaf.index(pk))
            ct += len(r2)
            ct += 10 * len([i for i in r2 if m[i] not in '0'+pk])
            li = [i in r1 and m[i] not in '0'+pk for i in r2[1:]]
            if isDead and li and any(li):
                ct += 100
        return ct
    put = lambda cur: q.put((g[cur] + heu(cur), cur)) if n > 0 else q.append(cur)
    get = lambda : q.get()[1] if n > 0 else q.pop(0)
    put(cur)
    while 1:
        if n == -2 and len(q) > 1:      # default
            break
        if n in [0,-1] and not q:      # default
            return mkd
        cur = get()
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
    cache[(n,s,e)] = res1
    return res1

def main(g_t,m,*a):
    global t,sy,sx,size,fx,fxli,cache,res
    t = g_t
    sy,sx = [[None,None],[None,None],[None,None]][t]
    size = sy * sx
    fx = {i:0 for i in range(size)}
    fxli = lambda li,n: fx.update({i:n for i in li})
    cache = {}
    res = []
    if t == 0:
        pass
    return res

if __name__ == '__main__':

    t,m1,m2 = 0,None,None

    ts = time()
    res = main(t,m1,m2)
    te = time() - ts
    print(res)
    # for i in res:
    #     print(i)
    print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
