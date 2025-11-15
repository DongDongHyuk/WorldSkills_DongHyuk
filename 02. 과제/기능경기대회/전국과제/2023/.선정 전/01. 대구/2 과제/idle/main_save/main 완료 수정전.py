from collections import deque
from time import time
from printer import printf

def exc(m,s,e,li,g=-1,p=-1):
    m = list(m)
    li = list(li) if t < 3 else None
    s2i = lambda n: ord(n)-87 if ord(n) > 96 else int(n)
    if g != -1:                                                 # 점, 선 정렬 - 팩을 잡거나 놓기
        m[s] = '0' if g else p
        li.append(p) if g else li.remove(p)
        return [(''.join(m),tuple(li)),[s,g,s2i(p),e]]         # [팩 놓을 위치,그리퍼,팩,타고 내려올 위치]
    m[s],m[e] = m[e],m[s]
    if t == 1 and m[s] == 'b':                                  # 선 정렬 - 다리 이동
        step = [e,s]
        m[e],m[e+(e-s)] = 'b','0'
        n = [i+sx for i in range(sx) if m[i+sx] != '0']
        if n:
            n, = n
            m[n+(s-e)],m[n] = m[n],'0'
        if m[s+sx] != '0':
            step = [e+(e-s),e]
        step += [m.index('b')]                                  # 다리 위치(앞쪽 기준) 
        step += [n,n+(s-e),int(m[n+(s-e)])] if n else [-1]*3    # [s,e,다리 위치,다리위의 팩 이동s,"e,팩]
    else:
        if t != 2:
            p = m[s]
            step = [e,s,s2i(p)]
        else:
            li = [1,-1] if li == [3,-3] else [3,-3]
            step = [e,s,int(m[e]),int(m[s])]
    return [(''.join(m),tuple(li)) if t < 3 else ''.join(m),step]

def aro(pos):
    if pos in cache:
        return cache[pos]
    res = []
    dy,dx = [([-1,0,1,0]*5,[0,1,0,-1]*5),([0,0,0,0]*5,[-3,-1,1,3]*5)][t==1]
    dz = [-2,-2,-2,-2,-1,-1,-1,-1,0,0,0,0,1,1,1,1,2,2,2,2]
    y,x,z = (pos // sx) % sy, pos % sx, pos // size
    for i in range(20):
        ny,nx,nz = y + dy[i],x + dx[i],z + dz[i]
        if -1 < ny < sy and -1 < nx < sx and -1 < nz < sz:
            n = ny * sx + nx + (size * nz)
            res.append(n)
    cache[pos] = res
    return res

def exp(n,m,pos=-1):
    res = []
    if t < 3:
        m,li = m
    for i in range(size*sz) if n else [pos]:        
        if t == 0 and m[i] not in '0b' and len(li) < 2 and \
            (i >= size*(sz-1) or m[i+size] == '0'):                                         # 점 정렬 - 팩 잡기            
                res.append(exc(m,i,-1,li,1,m[i]))
        if t == 0 and li and m[i] == '0' and \
           (i >= size*(sz-1) or m[i+size] == '0') and \
           (i < size*(sz-2) or m[i-size] != '0'):                                           # 점 - 팩 놓기
            for j in li:
                res.append(exc(m,i,-1,li,0,j))                
        if ((n and m[i] != '0') and t not in [1,2]) or i in fix:                            # i가 빈칸이 아닐때(선,면 정렬 제외), i가 고정일때
            continue        
        for j in [j for j in aro(i)
                  if m[j] not in ['x','0x'][n] and j not in fix]:
            if t == 0 and len(li) == 2:                                                    # 그리퍼 제한
                continue            
            if t == 0 or (t == 3 and n):                                                    # 점, 공간 정렬(정렬) - 3 차원 조건
                if (i >= size and m[i - size] == '0') or \
                    (j < size*(sz-1) and m[j + size] != '0'):
                        continue
            if t == 1:
                d = abs(i-j)
                if d == 1 and m[j] == 'b' and m[i] not in '0b' and len(li) < 1:            # 선 정렬 - 팩 잡기 
                    res.append(exc(m,i,-1,li,1,m[i]))                    
                if m[i] != '0':                                                            # 선 정렬 - i가 빈칸이 아닐때
                    continue
                if d == 1 and m[j] == 'b' and m[j+sx] == '0' and li:                       # 선 정렬 - 팩 놓기
                    for k in li:
                        res.append(exc(m,i,j,li,0,k))
                b0 = (m[j] in '135' and any([k in '135' for k in li])) or \
                     (m[j] in '246' and any([k in '246' for k in li]))                      # 공압, 그리퍼 제한                
                b1 = d in [sx-3,sx+3] or (i >= sx and m[i-sx] != 'b')                       # 이동 제한, 2층에 밑이 다리가 아닐때                
                b2 = m[j] == 'b' and m[sx:].count('0') < sx-1                               # 다리 이동 조건                
                b3 = d == 3 and (m[j] == 'b' or \
                                 m[i+((j-i)//3)] != 'b' or m[sx:].count('0') < sx)          # 다리 넘어 이동 조건                
                b4 = i >= sx and (m[i - sx] != 'b' or m[j] == 'b')                          # 다리위에 팩 적층 조건                
                if any([b0,b1,b2,b3,b4]):
                    continue
            if t == 2 and i-j not in li:
                continue                        
            res.append(exc(m,i,j,li if t < 3 else -1) if n else [j,j])            
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
            cur0,li = cur if t < 3 else (cur,None)
            if cur0 == leaf or \
               (pos != -1 and cur0[pos] == pack and \
                (t is not 1 or not li)):
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
    return m

def main(g_t,m,leaf=-1):    
    global t,sy,sx,sz,size,fix,res,cache
    t = g_t
    sy,sx,sz = [[1,2,3],[1,7,2],[3,3,1],[3,3,3]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}      # cache reset
    if t == 0:
        m,leaf = (m,()),'142530'
        bfs(1,m,leaf,-1,-1)
    if t == 1:
        m,leaf = (m,()),'1234bb00000000'
        for i in range(sx):
            m = bfs(1,m,leaf,i,leaf[i])
            fix.append(i)
    if t == 2:
        m,leaf = (m,(1,-1)),'123456789'
        for i in range(3):
            m = bfs(1,m,leaf,i,leaf[i])
            fix.append(i)
        bfs(1,m,leaf,-1,-1)
    if t == 3:
        for i in range(size*(sz-1)):
            if leaf[i] != '0':
                m = sort(m,leaf,i)
                if i < size*2:
                    fix.append(i)
        bfs(1,m,leaf,-1,-1)
    return res

if __name__ == '__main__':
    
##    Type,root,leaf = 0,'415320',-1
##    Type,root,leaf = 1,'2403bb10000000','1234bb0000000000'
##    Type,root,leaf = 2,'671348952',-1
    Type,root,leaf = 3,'9160b80cd0420e00530a7000000','de0ab07c0150060980400020030'

    ts = time()    
    res = main(Type,root,leaf)    
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
    
