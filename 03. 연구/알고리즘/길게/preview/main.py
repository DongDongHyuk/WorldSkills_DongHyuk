from time import time
from Tool.Printer import *

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    r = [e,s] if li == -1 else li
    info = [r,10+'abc'.index(m[s]) if m[s] in 'abc' else int(m[s])]
    return [''.join(m),info]

def aro(p):
    dxy = [-sx,1,sx,-1]
    li = [[(0,1,2,3),(3,7,11,15),(12,13,14,15),(0,4,8,12)],[],[]][t]
    return [p + dxy[i] for i in range(4) if p not in li[i]]

def exp(n,m,p=-1):
    res = []
    for i in range(size) if n > 0 else [p]:
        if (n > 0 and m[i] != '0') or fx[i]:
            continue
        for j in [j for j in aro(i) if m[j] not in ['x','0x'][n > 0] and not fx[j]]:            
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def src(n,m,*a):
    global res,mkdCt        # temp
    if n == 0:
        s,e = a
    if n == 1:
        p,pk = a
    q = [m if n > 0 else s] 
    mkd = {i:[] for i in q}
    while 1:
        cur = q.pop(0)
        if n > 0:       # temp
            mkdCt += 1
        if n == 0 and cur == e:
            break
        if n == 1:
            if (pk == -1 and cur == p) or (p != -1 and cur[p] == pk):
                break
        for i,j in exp(n,cur if n > 0 else m,cur):
            if i not in mkd:
                q.append(i)
                mkd[i] = mkd[cur] + [i]
    path = mkd[cur]
    if n > 0:
        res += path
        return cur
    return path
    
def sort(m,p,pk):
    r = src(0,m,m.index(pk),p)
    for i in r:
        m = src(1,m,i,pk)
    fx[p] = 1
    return m

def main(g_t,m,*a):
    global t,sy,sx,size,fx,fxli,res
    t = g_t
    sy,sx = [[4,4],[0,0],[0,0]][t]
    size = sy * sx
    fx = {i:0 for i in range(size)}         # temp(dict)
    fxli = lambda li,n: fx.update({i:n for i in li})
    res = []
    if t == 0:
        leaf, = a
        m = sort(m,0,'1')
    return res

if __name__ == '__main__':
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
