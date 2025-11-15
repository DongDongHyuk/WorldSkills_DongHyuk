from time import time
from printer import prt

def exc(m,s,e):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    info = [[e,s],int(m[s])]
    return [''.join(m),info]

def aro(p):
    dxy = [-sx,1,sx,-1]
    li = [[(0,1,2),(2,5,8),(6,7,8),(0,3,6)],
          [],
          []][t]
    return [p + dxy[i] for i in range(4) if p not in li[i]]

def exp(n,m,p=-1):
    res = []
    for i in range(size) if n > 0 else [p]:       
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
        leaf,p,pk = a
    cur = m if n > 0 else s
    q = [cur]
    mkd = {cur:[]}
    while 1:
        cur = q.pop(0)
        if n == 0 and cur == e:
            break
        if n == 1:
            if (p == -1 and cur == leaf) or (p != -1 and cur[p] == pk):
                break
        for i,j in exp(n,cur if n > 0 else m,cur):
            if i not in mkd:
                q.append(i)
                mkd[i] = mkd[cur] + [j]
    path = mkd[cur]
    if n > 0:
        res += path
        return cur
    return path
    
def sort(m,p,pk):
    r = bfs(0,m,m.index(pk),p)
    for i in r:
        m = bfs(1,m,-1,i,pk)
    fix.append(p)
    return m

def main(g_t,m,*a):    
    global t,sy,sx,size,fix,res
    t = g_t
    sy,sx = [[0,0],[0,0],[0,0]][t]
    size = sy * sx
    fix = []
    res = []
    if t == 0:
        pass
    return res

t,m,leaf = 0,'',''
ts = time()    
res = main(t,m,leaf)
te = time() - ts
print(res)
print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
