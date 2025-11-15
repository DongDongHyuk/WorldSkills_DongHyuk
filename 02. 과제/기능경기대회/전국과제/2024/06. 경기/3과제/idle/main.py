from collections import deque
from time import time
from printer import printf

def exc(m,s,e=-1,g=-1,p=-1,gli=-1,li=-1):
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
        step = li if li != -1 else [e,s]
    pack = 'abc'.index(pack)+10 if pack.isalpha() else int(pack)
    info = [s,g,pack,gp] if g != -1 else [step,pack]
    if g == -1 and m[e] != '0':
        info.append(int(m[e]))
    return [(''.join(m),tuple(gli)) if t == 3 else ''.join(m),info]
    
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
    if t == 3:
        m,gli = m
    res = []
    if t == 2:
        for i in range(8):
            for j in range(8):
                if i != j and all([k not in fix for k in [i,j]]):
                    res.append(exc(m,i,j))
        return res
    for i in range(size * sz) if n > 0 else [pos]: 
        if i in fix:
            continue
        if t == 3:
            if m[i] == '0' and gli.count('0') < 2 and (i > 5 or m[i + 2] == '0') and (i < 3 or m[i - 2] != '0'):        # put a pack
                for p in gli:
                    if p != '0':                        
                        res.append(exc(m,i,g=0,p=p,gli=gli))
            if gli.count('0') < 1:      # used all gripper
                continue
            if m[i] != '0' and (i > 5 or m[i + 2] == '0'):      # get a pack
                res.append(exc(m,i,g=1,gli=gli))
            continue
        if (n == -1 or n > 0) and m[i] != '0':
            continue
        for j in [j for j in aro(i) if m[j] not in ['x','0x'][n > 0] and j not in fix]:            
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def bfs(n,m,*a):
    global res
    if n == -1:
        s, = a
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 2:      # used A
        li,st,ct = a
    if n == 3:      # used A
        leaf,li = a
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n == -1 and m[cur] != '0':
            break
        if n == 0 and cur == e:
            break
        if n == 1:
            cur1 = cur[0] if t == 3 else cur
            if (pos == -1 and cur1 == leaf) or (pos != -1 and cur1[pos] == pack):
                break
        if n == 2:            
            if st[:ct] in ''.join([cur[i] for i in li if cur[i] != '0'])[:ct]:
                break
        if n == 3 and all([cur[i] == leaf[i] for i in li]):
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
    pack = leaf[e] if p == -1 else p
    b = len(exp(0,m,e)) == 1 
    if b:
        m = bfs(1,m,leaf,e,'0')
    s = m.index(pack)
    r = bfs(0,m,s,e)
    if b:
        fix.append(e)
    for i in r:
        if b and i in fix:
            fix.remove(i)
        m = bfs(1,m,leaf,i,pack)
    fix.append(e)
    return m

def main(g_t,m,*a):    
    global t,sy,sx,sz,size,fix,res,cache
    t = g_t
    sy,sx,sz = [[5,5,1],[4,4,1],[1,8,1],[1,2,4]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}      # cache reset
    if t == 0:
        leaf, = a
        hold = {}
        unhold = []
        leafc = leaf[:]
        for i in [1,3,5,9,15,19,21]:
            pack = leaf[i]
            if pack == '0' or pack in hold:
                r = [i]+bfs(-1,leafc,i)
                pos = r[-1]
                pack = leafc[pos]
                hold[pack] = r
                unhold.append(pack)
                leafc = list(leafc)
                leafc[pos] = '0'
                leafc = ''.join(leafc)
            m = sort(m,None,i,pack)        
        li1 = [6,7,8,13,18,17,16,11]
        li2 = [6,7,8,13,18,23,17,16,11]
        st = ''.join([leaf[i] for i in li2 if leaf[i] not in unhold + ['0']])
        for i in range(6):
            m = bfs(2,m,li1,st,i)        
        fix.append(23)
        if leaf[23] not in unhold + ['0']:
            m = bfs(1,m,leaf,18,leaf[23])
            m,step = exc(m,23,18)
            res.append(step)
        m = bfs(3,m,leaf,[leaf.index(m[i]) for i in li1 if m[i] != '0'])
        for pack in unhold[::-1]:
            r = hold[pack]            
            m,step = exc(m,r[-1],r[0],li=r)
            res.append(step)
    if t == 1:
        leaf, = a
        for i in [1,2,7,11,14,13,8,4]:
            m = sort(m,leaf,i)
    if t == 2:
        li = [1,0,2,3,4,5,6,7,8]
        for i in range(8):
            j = (4 + li[i]) % 8
            print(j,str(i+1))
            m = bfs(1,m,None,j,str(i+1))
            fix.append(j)
        res.append([[4,5],2,1])
    if t == 3:
        li = [sorted([i for i in m if i in st]) for st in ['2468','1357']]
        leaf = ['0']*8
        for i in range(2):
            li1 = li[i][::-1]
            for j in range(3):
                leaf[i+(2 * j)] = li1[j]
        m = (m,('0','0'))
        for i in range(6):
            m = bfs(1,m,None,i,leaf[i])
            fix.append(i)
    return res

if __name__ == '__main__':
    # t,m,leaf = 0,'x3x5x190a2xcx0x60b07x8x4x','x5x6x20b97x0xcx30a04x1x8x'
    # t,m,leaf = 1,'x10x05483726x00x','x21x30086004x75x'
    # t,m = 2,'64728153'
    # t,m = 3,'52631400'
    
    # t,m,leaf = 0,'x3x5x190a2xcx0x60b07x8x4x', 'x5x6x21b97x8xcx30a04x0x0x'
    # t,m,leaf = 1,'x10x05483726x00x', 'x21x30086004x75x'
    # t,m = 2,'64728153'
    t,m = 3,'52631400'

    ts = time()    
    res = main(t,m) if t > 1 else main(t,m,leaf)
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))


