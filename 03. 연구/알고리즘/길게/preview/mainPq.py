from time import time
from Tool.Printer import *
from queue import *

def exc(m,s,e):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    info = [[e,s],10+'abc'.index(m[s]) if m[s] in 'abc' else int(m[s])]
    return [''.join(m),info]

def aro(p):
    dxy = [-sx,1,sx,-1]
    li = [[(0,1,2,3),(3,7,11,15),(12,13,14,15),(0,4,8,12)],[],[]][t]
    return [p + dxy[i] for i in range(4) if p not in li[i]]

def exp(n,m,p=-1):
    res = []
    for i in range(size) if n > 0 else [p]:
        if (n > 0 and m[i] != '0') or i in fix:
            continue
        for j in [j for j in aro(i) if m[j] not in ['x','0x'][n > 0] and j not in fix]:            
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def src(n,m,*a):
    global res,mkdCt        # temp
    if n == 0:
        s,e = a
    if n == 1:
        leaf,p,pk =a
    cur = m if n > 0 else s
    pq = PriorityQueue()
    mkd = {cur:[]}
    put = lambda n: pq.put((len(mkd[n]),n))
    get = lambda : pq.get()[1]
    put(cur)
    while 1:
        cur = get()
        if n > 0:
            mkdCt += 1
        if n == 0 and cur == e:
            break
        if n == 1:
            if (p == -1 and cur == leaf) or (p != -1 and cur[p] == pk):               
                break
        for i,j in exp(n,cur if n > 0 else m,cur):
            if i not in mkd:
                mkd[i] = mkd[cur] + [i]
                put(i)
    path = mkd[cur]
    if n > 0:
        res += path
        return cur
    return path
    
def sort(m,p,pk):
    while m[p] != pk:
        r = src(0,m,m.index(pk),p)
        m = src(1,m,-1,r[0],pk)
    fix.append(p)
    return m

def main(g_t,m,*a):
    global t,sy,sx,size,fix,res
    t = g_t
    sy,sx = [[4,4],[0,0],[0,0]][t]
    size = sy * sx
    fix = []
    res = []
    if t == 0:
        leaf, = a
        m = sort(m,0,'1')
    return res

mkdCt = 0       # temp
t,m1,m2 = 0,'000cbxa987654321','12345x6789abc000'
ts = time()    
res = main(t,m1,m2)
te = time() - ts
# for i in res:
#     prt(i,4,4)
# print(res)
print('visited :',mkdCt)
te *= 3.5
print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
