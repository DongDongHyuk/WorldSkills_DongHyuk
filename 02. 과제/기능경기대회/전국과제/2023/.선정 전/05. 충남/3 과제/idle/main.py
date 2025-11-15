from collections import deque
from time import time
from printer import printf

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    step = [e,s] if li == -1 else li
    pack = int(m[s])
    info = [step,pack]
    m = (''.join(m),pack) if t == 2 else ''.join(m)
    return [m,info]
    
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
    if t == 2:
        m,p = m
    for i in range(size)[(4 if t == 1 else 0):] if n > 0 else [pos]:
        if (n > 0 and m[i] != '0') or i in fix:
            continue
        if t == 1 and (m[i] != '0' or m[i-4] == '0'):       # 3 차원 조건
            continue
        if t == 1:
            li = []
            for x in range(4):
                for z in range(4):
                    pos = z * 4 + x
                    if m[pos] != '0' and (z == 3 or (pos + 4 != i and m[pos+4] == '0')):
                        li.append(pos)
                        break
        if t == 2:
            li = [j % 8 for j in [i-3,i-2,i-1,i+1,i+2,i+3]]
        for j in [j for j in (li if t in [1,2] else aro(i))
                  if m[j] not in ['x','0x'][n > 0] and j not in fix]:
            if t == 0 and n == -1 and m[j] != '0':      #       
                continue
            if t == 2 and m[j] == p:        # 이전에 잡았던 팩
                continue
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def bfs(n,m,*a):
    global res
    if n < 1:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n < 1 and cur == e:
            break
        if n == 1:
            cur1 = cur[0] if t == 2 else cur
            if (pos == -1 and cur1 == leaf) or \
               (pos != -1 and cur1[pos] == pack):
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

def main(g_t,m,*a):    
    global t,sy,sx,size,fix,res,cache
    t = g_t
    sy,sx = [[4,5],[4,4],[1,8]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}      # cache reset
    if t == 0:
        s,e,li = a
        if e == -1:
            di = {}
            for i in range(4):
                e = li[i]
                try:
                    fix = [i for i in li if i != e]
                    di[e] = len(bfs(-1,m,s,e))
                except:
                    pass
            res = min(di,key = lambda n:di[n])  
        else:
            res = [s]+bfs(0,m,s,e)
    if t == 1:
        li, = a
        fix = [0,1,2,3]
        leaf = [m[i] for i in [0,1,2,3]]+['0']*12
        
        for i in range(4):
            pack = leaf[i]
            for j in range(li[i]-1):
                pos = 4 + i + (4 * j)
                leaf[pos] = pack
        leaf = ''.join(leaf)
        
        for i in [4,8,12]:
            m = bfs(1,m,leaf,i,leaf[i])
            fix.append(i)            
        m = bfs(1,m,leaf,-1,-1)        
    if t == 2:
        leaf = ['x' if i == 'x' else '0' for i in m]
        pos = 0
        for i in '112233':
            if leaf[pos] == 'x':
                pos += 1
            leaf[pos] = i
            pos += 1
        leaf = ''.join(leaf)
        m = bfs(1,(m,-1),leaf,-1,-1)
    return res

if __name__ == '__main__':

    ts = time()
    
##    t,m,s,e,li = 0,'000x0240300x00100x00',19,-1,[18,1,4,13]        # 가까운 리더기 찾기
    t,m,s,e,li = 0,'000x0240300x00100x00',18,0,-1      # A 길찾기
##    t,m,li = 1,'2231321310200000',[2, 2, 3, 3]
##    t,m = 2,'3310122x'      # 인덱스 정렬

    if t == 0:
        res = main(0,m,s,e,li)
    if t == 1:
        # 필요한 팩을 작은팩부터 왼쪽에서 오른쪽으로 가져온 맵을 받을거임
        res = main(t,m,li)
    if t == 2:
        res = main(t,m)
    
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res) if t != 0 else 'None ',round(te,3),int((te*250)//60),int((te*250)%60)))
