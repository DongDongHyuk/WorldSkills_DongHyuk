from collections import deque
from time import time
from printer import printf

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    step = [e,s] if li == -1 else li
    pack = 'abc'.index(m[s])+10 if m[s].isalpha() else int(m[s])
    info = [step,pack]
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

            if t == 1:
                if sorted([i,j]) in [[2,3],[8,9],[12,18],[13,19],[16,22],[17,23],[26,27],[32,33]]:
                    continue

            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def bfs(n,m,*a):
    global res
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 2:
        li,ct = a
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n == 0 and cur == e:
            break
        if n == 1:
            if (pos == -1 and cur == leaf) or \
               (pos != -1 and cur[pos] == pack):
                break
        if n == 2 and [cur[i] != '0' for i in li].count(1) >= ct:
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
    
def sort(m,leaf,e,p=-1):
    res = []
    pack = leaf[e] if p == -1 else p
    if pack != '0':
        s = m.index(pack)
        r = bfs(0,m,s,e)
        for i in r:
            m = bfs(1,m,leaf,i,pack)
    else:
        m = bfs(1,m,leaf,e,'0')
    fix.append(e)
    return m

def main(g_t,m,*a):    
    global t,sy,sx,size,fix,res,cache
    t = g_t
    sy,sx = [[0,0],[6,6],[0,0]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {} 
    if t == 1:
        pass
    if t == 1:
        leaf = 'x0000xxx00xx123456cba987xx00xxx0000x'
        li = [[1,2,8],[3,4,9],[26,31,32],[27,33,34]]
        li1 = []
        di = {'1':12,'2':13,'3':14,'4':15,'5':16,'6':17,'7':23,'8':22,'9':21,'a':20,'b':19,'c':18}
        ct = 12
        for pack in '1c672b58':
            fix = li1[:]

            n, = [i for i in range(4) if pack in [m[i] for i in li[i]]]
            for i in range(4):
                if i != n:
                    fix += li[i]
            pos = di[pack]
            m = bfs(1,m,leaf,pos,pack)
            fix.append(pos)
            li1.append(pos)
            ct -= 1
            m = bfs(2,m,li[0]+li[1]+li[2]+li[3],ct)
        fix = [12,13,16,17,18,19,22,23]

    if t == 2:
        pass
    return res

if __name__ == '__main__':

    t,m = 1,'x9685xxx21xx000000000000xx7cxxxa3b4x'
        
    ts = time()    
    res = main(t,m)    
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
