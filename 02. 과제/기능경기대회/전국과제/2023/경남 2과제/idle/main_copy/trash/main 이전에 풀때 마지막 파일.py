from collections import deque
from time import time
from printer import printf

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    step = [e,s] if li == -1 else li
    pack = 'abc'.index(m[s])+10 if m[s].isalpha() else int(m[s])
    info = ([ing] if t == 0 else [])+[step,pack]
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

def exp(n,m,pos=-1,p:'B 파레트 길찾기' = -1):
    res = []
    if t == 0:
        hli0 = hli[ing]
    if t == 1:
        hli0 = hli[:]
    for i in range(size) if n > 0 else [pos]:
        if (n > 0 and m[i] != '0') or i in fix:
            continue
        if t < 2 and n > 0 and i in hli0:
            continue
        for j in aro(i):
            b = lambda pos: \
                m[pos] not in (['0x','x'][t < 2] if n > 0 else 'x') and pos not in fix
            if not b(j):
                continue
            if t < 2 and n > 0:
                if j in hli0:
                    li = [j]
                    for hp in li:           # hole position
                        li0 = [li[0]] + ([] if hp == li[0] else [hp])        # 'li' init state coped                        
                        for k in aro(hp):
                            if not b(k) or k in li:
                                continue
                            if m[k] == '0':
                                if k in hli0:
                                    li.append(k)
                                continue
                            if t is 1:
                                if (hli0[1] in li0 and m[k] in '789abc') or \
                                   (hli0[2] in li0 and m[k] in '123456'):
                                    continue 
                            res.append(exc(m,i,k,([i]+li0+[k])[::-1]))                        
                if m[j] == '0':
                    continue
            if t == 1 and n < 1 and p != -1:
                if (p in '123456' and j == hli0[2]) or \
                   (p in '789abc' and j == hli0[1]):
                    continue
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def bfs(n,m,*a,p:'B 파레트 길찾기' = -1):
    global res,fix
    if n < 1:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 2:
        li, = a
    if n == 3:
        leaf,li = a
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        if n == -1 and not que:
            if e == -1:
                return list(mkd.keys())
            return -1
        cur = que.popleft()
        if n < 1 and cur == e:
            break
        if n == 1:
            if (pos == -1 and cur == leaf) or \
               (pos != -1 and cur[pos] == pack):
                break
        if n == 2 and all([cur[i] == '0' for i in li]):
            break
        if n == 3:
            if all([cur[i] == leaf[i] for i in li]):
                break        
        for i,j in exp(n,cur if n > 0 else m,cur,
                       p if t == 1 and p != -1 else -1):
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
        
def sort(m,leaf,e,p = -1):
    global fix,res
    pack = leaf[e] if p is -1 else p    
    s = [i for i in range(size) if i not in fix and m[i] == pack][0]        # A,C 가 팩이 여러개라 이렇게 함
    r = bfs(0,m,s,e)
    if not t:
        r = [i for i in r if i not in hli[ing]]
    for i in r:
        m = bfs(1,m,leaf,i,pack)        
    fix.append(e)
    return m

def main(g_t,m,*a):    
    global t,sy,sx,size,fix,res,cache
    t = g_t
    sy,sx = [[3,5],[4,5],[3,4]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}      # cache reset
    if t in [0,1]:
        global hli
    if t == 1:
        pass
    if t == 2:
        pass
    
    return res

if __name__ == '__main__':
    
##    t,m1,m2,a = 0,'051002426053060','510642030314000',[[0, 9, 14], [2, 6, 12]]
##    t,m1,m2,a = 1,'605a0709038400c0b201','60c50903a0020871040b',[4, 6, 12]          # hmi 예시 배치
        
    ts = time() 
    res = main(t,m1,m2,a)
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,6),int((te*250)//60),int((te*250)%60)))
