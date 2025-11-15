from collections import deque
from time import time
from printer import printf

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    step = [e,s] if li == -1 else li
    info = [step,int(m[s])]
    return [''.join(m),info]
    
def aro(pos):
    if pos in cache:
        return cache[pos]
    res = []    
    if t == 2:
        dy,dx = [-1,0,1,0,-1,1,1,-1],[0,1,0,-1,1,1,-1,-1]
    else:
        dy,dx = [-1,0,1,0],[0,1,0,-1]
    y,x = divmod(pos,sx)
    for i in range(8):
        ny,nx = y + dy[i],x + dx[i]
        if -1 < ny < sy and -1 < nx < sx:
            res.append(ny * sx + nx)
    cache[pos] = res
    return res

def exp(n,m,pos=-1,pack=-1):
    res = []
    if n < 1:         # 길찾기
        for i in [i for i in aro(pos) if i not in fix and m[i] != 'x']:
            if t == 2:
                b1 = n == -1 and m[i] != '0'
                b2 = i in hli
                b3 = (abs(pos - i) in [1,5] and pack in '5678') or \
                     (abs(pos - i) in [4,6] and pack in '1234')
                if any([b1,b2,b3]):
                    continue
            res.append([i,i])
    else:       # 정렬
        for i in range(size):
            pack = m[i]
            if i in fix or pack in '0x':
                continue
            mkd,step = bfs(-1,m,i,p = pack)
            for j in mkd:
                if i != j:
                    res.append(exc(m,j,i,[i]+path(mkd,step,j)))
    return res

def bfs(n,m,*a,p:'길찾기'=-1):
    global res
    if n == -1:
        s, = a
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 2:
        li1,li2 = a
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        if n == -1 and not que:
            return mkd,step
        cur = que.popleft()
        if n == 0 and cur == e:
            break
        if n == 1:
            if (pos == -1 and cur == leaf) or \
               (pos != -1 and cur[pos] == pack):
                break
        if n == 2 and \
           all([cur[i] == '0' for i in li1]) and \
           all([cur[i] != '0' for i in li2]):
            break
        for i,j in exp(n,cur if n > 0 else m,cur,p):
            if i not in mkd:
                que.append(i)
                mkd[i],step[i] = cur,j
    mkd[-2] = cur
    res0 = path(mkd,step)
    if n > 0:
        res += res0
        return mkd[-2]
    return res0

def path(mkd,step,cur=-1):
    cur = cur if cur != -1 else mkd[-2]
    path = [step[cur]]
    while mkd[cur] != -1:
        cur = mkd[cur]
        path.append(step[cur])
    return path[::-1][1:]
    
def sort(m,leaf,e,p=-1):
    pack = leaf[e] if p == -1 else p
    if pack == '0':
        return m
    res = []
    s = m.index(pack)
    r = bfs(0,m,s,e,p = pack)


    
    return m

def main(g_t,m,*a):    
    global t,sy,sx,size,fix,res,cache
    t = g_t
    sy,sx = [[4,4],[4,5],[5,5]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}      # cache reset
    if t == 0:
        pass
    if t == 1:
        pass
    if t == 2:
        global hli
        leaf,hli = a

        li = [i for i in [4,9,14,19,24] if i not in hli]
        for i in range(len(li)+1):
            m = bfs(2,m,[],li[:i])
        fix += li

        

        printf(m,5,5)
        printf(leaf,5,5)
        
    return res

    
t,m1,m2,a = 2,'0057006218304000000000000','5008106400000000300702000',[15, 22]

ts = time()    
res = main(t,m1,m2,a)    
te = time() - ts
print(res)
print("{}step, idle {}s(dart {}m {}s) \n".
format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
