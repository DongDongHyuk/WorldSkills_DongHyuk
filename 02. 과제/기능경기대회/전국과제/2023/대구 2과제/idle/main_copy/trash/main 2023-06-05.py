from collections import deque
from functools import lru_cache

from time import time
from printer import printf
from rdm import rdm

def exc(m,s,e):
    m = list(m)
    m[s],m[e] = m[e],'0'
    if t == 1 and m[s] == 'b':
        m[e],m[e+(e-s)] = 'b','0'
        dq = deque(m[9:])
        dq.rotate(s-e)
        m = m[:9]+list(dq)
        if m[s+9] != '0':
            return [''.join(m),[e+(e-s),e]]
    return [''.join(m),[e,s]]

@lru_cache(maxsize=None)
def aro(t,pos):
    res = []
    dy,dx = ([-1,0,1,0]*5,[0,1,0,-1]*5) if t != 1 else \
            ([0,0,0,0]*5,[-3,-1,1,3]*5)
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
    for i in range(size*sz) if n else [pos]:
        if (n and m[i] != '0') or i in fix:
            continue
        for j in [j for j in aro(t,i)
                  if m[j] not in ['x','0x'][n] and j not in fix]:
            
            if t == 1:
                
                '''
                09 10 11 12 13 14 15 16 17
                00 01 02 03 04 05 06 07 08
                '''
                
                # 다리 넘어 이동 조건
                d = abs(i-j)
                if (i > 8 and  d == 3) or d in [6,12]:
                    continue
                if d == 3:
                    a,b = (i+1,i+2) if i < j else (i-1,i-2)
                    if [k for k in [0,9] if m[a+k]+m[b+k] != ('00' if k else 'bb')]:
                        continue
                
                # 다리 이동 조건
                # 누은팩위에 팩 적층 조건
                if m[j] == 'b' and m[9:].count('0') == 2 or \
                   (i > 8 and (m[i - 9] != 'b' or m[j] == 'b')):
                    continue
                
            if t == 3 and n:
                if (i >= size and m[i - size] == '0') or \
                    (j < size*(sz-1) and m[j + size] != '0'):
                        continue

            res.append(exc(m,i,j) if n else [j,j])
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
            if cur == leaf or \
                (pos != -1 and cur[pos] == pack):
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
    
    if t == 1:

        print(' ROOT \n')
        printf(m,1,9,2)

        print('>>> \n')

        res = exp(1,m)
        for i in range(len(res)):
            print(res[i][1])
            printf(res[i][0],1,9,2)
    
    if t == 3:
        for i in range(size*(sz-1)):
            if leaf[i] != '0':
                m = sort(m,leaf,i)      # short bfs                
        m = bfs(1,m,leaf,-1,-1)         # default bfs
        
    return res

if __name__ == '__main__':
    ts = time()

    # A 파레트(점 정렬)
##    Type,root,leaf = 0,None,None
##    res = main(Type,3,3,3,root)

    # B 파레트(선 정렬)
    Type,root,leaf = 1,'40bb05136'+'000200000','123456bb0'+'0'*9
    res = main(Type,1,9,2,root)

    # C 파레트(면 정렬)
##    Type,root,leaf = 2,None,None
##    res = main(Type,3,3,3,root)

    # D 파레트(공간 정렬)
##    Type,root,leaf = 3,'30d59eca000071b860000004200','5d7b604e03208a00009c0100000'
##    res = main(Type,3,3,3,root)
    
    te = time() - ts
##    print(res)
    print(len(res),'step','{}s'.format(round(te,3)))


# 그리퍼 구현만 하면됨 선정렬 

