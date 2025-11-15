from collections import deque
from time import time
from printer import printf

def exc(m,s,e=-1,g=-1,p=-1,gli=-1):
    m = list(m)
    if g != -1:
        isg = g == 1
        pack = m[s] if isg else p
        gp = gli.index('0' if isg else p)
        gli = list(gli)
        gli[gp] = pack if isg else '0'
        m[s] = '0' if isg else p
    else:
        m[s],m[e] = m[e],m[s]
        pack = m[s]
        if t == 0:
            gp = gli.index('0')
    pack = ('abc'.index(pack)+10 if pack.isalpha() else int(pack)) + [0,12,18,24][t]
    info = [s,g,pack,gp] if g != -1 else [[e,s],pack]
    if t == 0 and g == -1:
        info.append(gp)
    return [(''.join(m),tuple(gli)) if t == 0 else ''.join(m), info]
    
def aro(pos):
    if pos in cache:
        return cache[pos]
    res = []
    if t == 2:
        di = {1:3,3:1,6:8,8:6,11:13,13:11}
        if pos in di:
            res = [di[pos]]
    dy,dx = [-1,0,1,0]*3,[0,1,0,-1]*3
    dz = [-1,-1,-1,-1,0,0,0,0,1,1,1,1]
    y,x,z = (pos // sx) % sy, pos % sx, pos // size
    for i in range(12):
        ny,nx,nz = y + dy[i],x + dx[i],z + dz[i]
        if -1 < ny < sy and -1 < nx < sx and -1 < nz < sz:
            n = ny * sx + nx + (size * nz)
            res.append(n)
    cache[pos] = res
    return res

def exp(n,m,pos=-1,pack=-1):
    if t == 0:
        m,gli = m
    res = []
    for i in range(size * sz) if n > 0 else [pos]:
        if i in fix:       # default rule
            continue
        if t == 0:      # A rule
            if m[i] == '0' and gli.count('0') < 2 and (i > 5 or m[i + 6] == '0') and (i < 6 or m[i - 6] != '0'):        # put a pack
                for p in gli:
                    if p != '0':                        
                        res.append(exc(m,i,g=0,p=p,gli=gli))
            if gli.count('0') < 1:      # used all gripper
                continue
            if m[i] != '0' and (i > 5 or m[i + 6] == '0'):      # get a pack
                res.append(exc(m,i,g=1,gli=gli))
        if n > 0 and m[i] != '0':       # default rule
            continue
        if t == 2:      # C rule
            if i in [2,7,12]:
                continue
        for j in [j for j in aro(i) if m[j] not in ['x','0x'][n > 0] and j not in fix]:            
            if t == 0:      # A rule
                if (i > 5 and m[i - 6] == '0') or (j < 6 and m[j + 6] != '0'):
                    continue
            if t == 2:      # C rule
                if abs(i - j) == 2:       # 홀 팩 조건  
                    h, = [k for k in hli if (k - 1) in [i,j]]
                    if any([(m[j] if n > 0 else pack) in st and h != hli[k] for k,st in enumerate(['14','25','36'])]):
                        continue
            res.append(exc(m,i,j,gli = gli if t == 0 else -1) if n > 0 else [j,j])
    return res

def bfs(n,m,*a):
    global res
    runM = m[1] if t == 3 and len(m) == 2 else -1
    if runM != -1:
        m = m[0]
    if n == 0:
        if t == 2:
            s,e,pack = a
        else:
            s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 2:      # used B
        pos,pack1,pack2 = a
    if n == 3:      # used C
        li,ct = a
    if n == 4:      # used C
        leaf,li,ct = a
    if n == 5:      # used D
        pos,li = a
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n == 0 and cur == e:
            break
        if n == 1:
            cur1 = cur[0] if t == 0 else cur
            if (pos == -1 and cur1 == leaf) or (pos != -1 and cur1[pos] == pack):
                break
        if n == 2 and (pos == -1 or cur[0][pos] == pack1) and pack2 in cur[1]:
            break
        if n == 3 and [cur[i] for i in li].count('0') == ct:
            break
        if n == 4 and [cur[i] == leaf[i] for i in li].count(1) >= ct:
            break
        if n == 5 and cur[pos] in li:
            break
        for i,j in exp(n,(cur if n > 0 else m),(cur if n < 1 else -1),(pack if n < 1 and t == 2 else -1)):
            if i not in mkd:
                que.append(i)
                mkd[i],step[i] = cur,([runM] + j if runM != -1 else j)
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
    pack = leaf[e] if p == -1 else p
    if t == 3:
        m,j = m
    s = m.index(pack)
    if t == 2:
        r = bfs(0,m,s,e,pack)
    else:
        r = bfs(0,m,s,e)        
    for i in r:
        m = bfs(1,(m,j) if t == 3 else m,leaf,i,pack)
    fix.append(e)
    return m

def main(g_t,m,*a):    
    global t,sy,sx,sz,size,fix,res,cache
    t = g_t
    sy,sx,sz = [[1,6,2],[3,3,1],[3,5,1],[3,3,1]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}      # cache reset
    if t == 0:
        m = (m,('0','0'))
        leaf = '123456cba987'
        for i in [0,6,1,7,2,8,3,9,4,10]:
            pack = leaf[i]
            m = bfs(2,m,-1,-1,pack)
            for j in range(i, -1, -6):
                if j not in fix:
                    m = bfs(2,m,j,'0',pack)
            m = bfs(1,m,leaf,i,pack)
            fix.append(i)
        m = bfs(1,m,leaf,-1,-1)        
    if t == 1:
        leaf = '123456000'
        for i in range(6):
            m = sort(m,leaf,i,leaf[i])
    if t == 2:
        global hli
        hli, = a
        leaf = '01040x205x03060'
        li = [0,10,1]
        for i in range(1,4):
            m = bfs(3,m,li,i)
        fix = [10]
        m = sort(m,leaf,0,'1')
        fix = [0]
        li = [3,6,8,11,13]
        for i in range(1,6):
            m = bfs(4,m,leaf,li,i)
        fix = []
        m = bfs(1,m,leaf,-1,-1)
    if t == 3:
        m2, = a
        m1 = m[:]
        leaf1,leaf2 = '123456000','0a70b80c9'
        red = [5,1]
        blue = [7,3]
        for i in range(6 - len([i for i in m1 if i in '123456'])):
            for j in range(2):
                mc1,mc2 = [m1,m2][j][:],[m2,m1][j][:]
                h1,h2 = red[1] if j else blue[0],red[0] if j else blue[1]
                mc1 = bfs(5,(mc1,j),h1,'123456' if j else '789abc')
                mc2 = bfs(1,(mc2,(1 - j)),None,h2,'0')
                mc1,mc2 = map(list,[mc1,mc2])
                mc1[h1],mc2[h2] = mc2[h2],mc1[h1]
                mc1,mc2 = map(''.join,[mc1,mc2])
                m1,m2 = [mc1,mc2][j][:],[mc2,mc1][j][:]
                pack = ('abc'.index(mc2[h2])+10 if mc2[h2].isalpha() else int(mc2[h2])) + [0,12,18,24][t]
                res.append([j,pack]) 
        for j in range(2):
            m,leaf = [m1,m2][j][:],[leaf1,leaf2][j][:]
            fix = []
            for i in [2,5,8,1,4,7] if j else range(6):
                m = sort((m,j),leaf,i,leaf[i])
    return res

if __name__ == '__main__':

    # t,m = 0,'b7c61298a435'    
    # t,m = 1,'401356020'
    # t,m,hli = 2,'45061x000x30020',[12, 2, 7]
    # t,m1,m2 = 3,'b0518700a', '39204006c'

    # t,m = 0,'2719683a4c5b'
    # t,m = 1,'504310026'
    # t,m,hli = 2,'05060x104x02030',[2, 12, 7]
    # t,m1,m2 = 3,'0a15b0902', '0c4836070'

    ts = time()    
    res = main(t,m) if t in [0,1] else main(t,m1,m2) if t == 3 else main(t,m,hli)
    te = time() - ts

    # Printing Path
    print(res)
    # if t == 0:
    #     for m,gli in res:
    #         print('gli ->',gli)
    #         printf(m,1,6,2)
    # if t in [1,2]:
    #     for m in res:
    #         printf(m,sy,sx,sz)

    # Printing RunTime
    print("{}step, idle {}s(dart {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
