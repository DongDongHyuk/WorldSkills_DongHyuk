from collections import deque
from functools import lru_cache

from time import time
from printer import printf
from rdm import rdm

def exc(m,s,e,gli,pack=-1):
    m = list(m)
    if e == -1:
        m[s],gli = gli,pack
        return ((''.join(m),gli),
                [s,-1 if gli == '0' else 1,pack])
    m[s],m[e] = m[e],'0'
    if t == 1 and m[s] == 'b':
        m[e],m[e+(e-s)] = 'b','0'
        n = [i+sx for i in range(sx) if m[i+sx] != '0']
        if n:       # 다리위에 팩이 있을때
            n, = n
            m[n+(s-e)],m[n] = m[n],'0'
        if m[s+sx] != '0':
            return ((''.join(m),gli),[e+(e-s),e])
    return ((''.join(m),gli) if t == 1 else ''.join(m),[e,s])

@lru_cache(maxsize=None)
def aro(t,pos):
    res = []
    dy,dx = [([-1,0,1,0]*5,[0,1,0,-1]*5),([0,0,0,0]*5,[-3,-1,1,3]*5)][t==1]
    dz = [-2,-2,-2,-2,-1,-1,-1,-1,0,0,0,0,1,1,1,1,2,2,2,2]
    y,x,z = (pos // sx) % sy, pos % sx, pos // size
    for i in range(20):
        ny,nx,nz = y + dy[i],x + dx[i],z + dz[i]
        if -1 < ny < sy and -1 < nx < sx and -1 < nz < sz:
            n = ny * sx + nx + (size * nz)
            res.append(n)
    return res

def exp(n,m,pos=-1):
    res = []
    if t == 1:
        m,gli = m       # 맵, 그리퍼가 가지고 있는팩
    for i in range(size*sz) if n else [pos]:        
        if t == 1 and m[i] not in '0b' and gli == '0':
            res.append(exc(m,i,-1,gli,m[i]))        
        if (n and m[i] != '0') or i in fix:
            continue
        for j in [j for j in aro(t,i)
                  if m[j] not in ['x','0x'][n] and j not in fix]:            
            if t == 1:                
                d = abs(i-j)
                if d == 1 and m[j] == 'b' and m[j+sx] == '0' and gli != '0':                # 가지고 있던팩 놓기
                    res.append(exc(m,i,-1,gli,'0'))
                b0 = (gli in '135' and m[j] in '135') or \
                     (gli in '246' and m[j] in '246')                                       # 공압, 그리퍼 제한
                b1 = d in [sx-3,sx+3] or (i >= sx and m[i-sx] != 'b')                       # 이동 제한, 2층에 밑이 다리가 아닐때 컨티뉴
                b2 = m[j] == 'b' and m[sx:].count('0') < sx-1                               # 다리 이동 조건
                b3 = d == 3 and \
                     (m[j] == 'b' or m[i+((j-i)//3)] != 'b' or m[sx:].count('0') < sx)      # 다리 넘어 이동 조건     
                b4 = i >= sx and (m[i - sx] != 'b' or m[j] == 'b')                          # 다리위에 팩 적층 조건                
                if any([b0,b1,b2,b3,b4]):
                    continue                
            if t == 3 and n:
                if (i >= size and m[i - size] == '0') or \
                    (j < size*(sz-1) and m[j + size] != '0'):
                        continue
            res.append(exc(m,i,j,gli if t == 1 else -1) if n else [j,j])
    return res

def bfs(n,m,*a):
    global res
    if n:
        leaf,pos,pack = a
    else:
        s,e = a        
    cur = m if n else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n:
            cur0,gli = cur if t == 1 else (cur,None)
            if cur0 == leaf or \
               (pos != -1 and (cur0[pos] == pack and gli in [None,'0'])):
                    break
        elif cur == e:
            break
        for i,j in exp(n,cur if n else m,cur):
            if i not in mkd:
                que.append(i)
                mkd[i],step[i] = cur,j
    mkd[-2] = cur
    path = [step[cur]]
    while mkd[cur] != -1:
        cur = mkd[cur]
        path.append(step[cur])
    if n:
        res += path[::-1][1:]
        return mkd[-2]
    return path[::-1][1:]
    
def sort(m,leaf,e):
    pack = leaf[e]
    res = []
    s = m.index(pack)
    road = [s]+bfs(0,m,s,e)
    for i in range(len(road)):
        n = road[i]
        if t == 3 and n < 16:
            if i:
                fix.append(road[i-1])
                fix.append(road[i-1]+9)
            m = bfs(1,m,leaf,n+9,'0')
            if i:
                del fix[-2:]        
        m = bfs(1,m,leaf,n,pack)
    fix.append(e)
    return m

def main(g_t,y,x,z,m,*a):    
    global t,sy,sx,sz,size,fix,res
    t = g_t
    sy,sx,sz = y,x,z
    size = sy * sx
    fix = []
    res = []
    
    if t == 0:
        printf(m,1,2,3)
        
    if t == 1:
        
        m = (m,'0')
        for i in range(sx):
            m = bfs(1,m,leaf,i,leaf[i])
            fix.append(i)
        bfs(1,m,leaf,-1,-1)

##        m = (m,'0')
##        for i,step in exp(1,m):
##            print('step :',step,'|','gli :',i[1])
##            printf(i[0],1,7,2)
        
    if t == 3:
        for i in range(size*(sz-1)):
            if leaf[i] != '0':
                m = sort(m,leaf,i)      # short bfs                
        bfs(1,m,leaf,-1,-1)             # default bfs
        
    return res

if __name__ == '__main__':
    ts = time()

##    Type,root,leaf = 0,'514230','142530'
##    res = main(Type,1,2,3,root)

    Type,root,leaf = 1,'42031bb0000000','1234bb00000000'
    res = main(Type,1,7,2,root)

##    Type,root,leaf = 2,None,None
##    res = main(Type,3,3,3,root)

##    Type,root,leaf = 3,'30d59eca000071b860000004200','5d7b604e03208a00009c0100000'
##    res = main(Type,3,3,3,root)
    
    te = time() - ts
    print(res)
    print(len(res),'step','{}s'.format(round(te,3)))



    
