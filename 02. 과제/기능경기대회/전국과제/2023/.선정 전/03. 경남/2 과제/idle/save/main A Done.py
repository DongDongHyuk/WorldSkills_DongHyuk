from collections import deque
from time import time
from printer import printf

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    step = [e,s] if li is -1 else li
    info = ([ing] if t is 0 else [])+[step,int(m[s])]
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
    hli0 = hli[ing]
    for i in range(size) if n > 0 else [pos]:       
        if (n > 0 and m[i] != '0') or i in fix:
            continue
        if t is 0 and n > 0 and i in hli0:
            continue
        for j in aro(i):
            b = lambda pos: \
                m[pos] not in (['0x','x'][t is 0] if n > 0 else 'x') and pos not in fix
            if not b(j):
                continue
            if t is 0 and n > 0:
                if j in hli0:
                    li = [j]
                    for hp in li:           # hole position
                        li0 = li[:]         # 'li' init state coped
                        for k in aro(hp):
                            if b(k) and k not in li:
                                if m[k] == '0':
                                    if k in hli0:
                                        li.append(k)
                                    continue
                                res.append(exc(m,i,k,([i]+li0+[k])[::-1]))
                if m[j] == '0':
                    continue
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def bfs(n,m,*a):
    global res
    if n is 0:
        s,e = a
    if n is 1:
        leaf,pos,pack = a
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n is 0 and cur is e:
            break
        if n is 1:
            if (pos is -1 and cur == leaf) or \
               (pos is not -1 and cur[pos] == pack):
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
    pack = leaf[e] if p is -1 else p
    res = []
    s = [i for i in range(size) if i not in fix and m[i] == pack][0]
    r = bfs(0,m,s,e)
    if t is 0:
        r = [i for i in r if i not in hli[ing]]
    for i in r:
        m = bfs(1,m,leaf,i,pack)
    fix.append(e)
    return m

def main(g_t,m,*a):    
    global t,sy,sx,size,fix,res,cache
    t = g_t
    sy,sx = [[3,5],[0,0],[0,0]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}      # cache reset
    if t is 0:
        global hli,ing
        m1 = m[:]
        m2,hli = a
        # pack exchanging
        m1,m2 = map(list,[m1,m2])        
        for i in range(15):
            if m1[i] in '456':
                j = [j for j in range(15) if m2[j] in '123'][0]
                m1[i],m2[j] = m2[j],m1[i]
                res.append([i,j,m1[i],m2[j]])
        m1,m2 = map(''.join,[m1,m2])
        # make leaf
        leaf = []
        for i in range(2):
            m0 = ['0'] * 15
            ct = [-1,0,0,0,0,0,0]
            li = ([j for j in range(15) if leaf[0][j] == '0'] if i else [])+list(range(15)) 
            for j in hli[1-i]+li:
                pack = j // 5 + (3 * i) + 1
                if j not in hli[i] and m0[j] is '0' and ct[pack] < 3:
                    m0[j] = str(pack)
                    ct[pack] += 1
            leaf.append(''.join(m0))
        leaf1,leaf2 = leaf
        for i in range(2):
            ing = i         # now sorting
            m = [m1,m2][i]
            leaf = [leaf1,leaf2][i]            
            for j in [0,1,2,3,4]:
                if j in hli[i] or leaf[j] == '0':
                    m = bfs(1,m,leaf,j,'0')
                    fix.append(j)
                    pass
                else:
                    m = sort(m,leaf,j)
            m = bfs(1,m,leaf,-1,-1)
            if i:
                m2 = m[:]
            else:
                m1 = m[:]
            fix = []        # fix reset
    return res

if __name__ == '__main__':
    
    Type,m1,m2,a = 0,'051002426053060','510642030314000',[[0, 9, 14], [2, 6, 12]]

    ts = time()    
    res = main(Type,m1,m2,a)    
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
