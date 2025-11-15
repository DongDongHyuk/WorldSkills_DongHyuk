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
    di = {3:[11], 11:[3,23], 23:[11,27], 27:[23],26:[18], 18:[6,26], 6:[2,18], 2:[6]}
    res = di[pos] if t == 0 and pos in di else []
    dy,dx = [-1,0,1,0],[0,1,0,-1]
    y,x = divmod(pos,sx)
    for i in range(4):
        ny,nx = y + dy[i],x + dx[i]
        if -1 < ny < sy and -1 < nx < sx:
            n = ny * sx + nx
            if t == 0 and sorted([pos,n]) in [[6,7],[10,11],[18,19],[22,23]]:
                continue
            res.append(n)
    cache[pos] = res
    return res

# A 홀 조건 추가
def exp(n,m,pos=-1):
    res = []
    for i in range(size) if n > 0 else [pos]:

        if (n > 0 and (m[i] != '0' or i in hli)) or i in fix:
            continue

        for j  in aro(i):
            b = lambda j: m[j] in 'x' or j in fix    
            if b(j):
                continue 

            if t == 0 and n > 0 and j in hli:         # A 파레트 홀 이동 조건
                que = deque([j])
                mkd = {j:i,i:-1}
                while que:
                    cur = que.popleft()
                    for k in aro(cur):
                        if k not in mkd:                                
                            mkd[k] = cur
                            if k in hli:
                                que.append(k)
                            if m[k] == '0' or b(k):
                                continue
                            res1 = path(mkd,mkd,k)+[k]
                            res.append(exc(m,i,k,res1[::-1])) 

            if n > 0 and m[j] == '0':
                continue

            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def bfs(n,m,*a):
    global res
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 2:      # used A
        li, = a

    if n == 3:      # used A
        li1,li2,ct1,ct2 = a

    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n == 0 and cur == e:
            break
        if n == 1:
            if (pos == -1 and cur == leaf) or (pos != -1 and cur[pos] == pack):
                break
        if n == 2 and [cur[i] for i in li].count('0') < 2:
            break

        if n in [3,4]:
            count1,count2 = 0,0
            li3,li4 = map(lambda li:[cur[i] for i in li],[li1,li2])
            if n == 3:
                for i in range(4):
                    pack = li3[i]
                    if pack != '0':
                        count1 += 1 if pack in li4 else 0
                        count2 += 1 if pack == li4[i] else 0
            if count1 >= ct1 and count2 >= ct2:
                break

        for i,j in exp(n,cur if n > 0 else m,cur):
            if i not in mkd:
                que.append(i)
                mkd[i],step[i] = cur,i
    res1 = path(mkd,step,cur)    
    if n > 0:
        res += res1
        return cur
    return res1

def path(mkd,step,cur):
    path = [step[cur]]
    while mkd[cur] != -1:
        cur = mkd[cur]
        path.append(step[cur])
    return path[::-1][1:]
    
def sort(m,leaf,e,p=-1):
    pack = leaf[e] if p == -1 else p
    s = [i for i in range(size) if m[i] == pack and i not in fix][0]
    r = bfs(0,m,s,e)
    for i in r:
        if t == 0 and i in hli:
            continue
        m = bfs(1,m,leaf,i,pack)
    fix.append(e)
    return m

def main(g_t,m,*a):    
    global t,sy,sx,size,fix,res,cache
    t = g_t
    sy,sx = [[5,6],[0,0],[0,0]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}      # cache reset
    if t == 0:
        global hli
        hli, = a
        # 중앙 정렬
        li = [[7,10],[13,16],[14,15]] if m[8] == 'x' else [[19,22],[13,16],[14,15]]
        li = [i for i in li if i != hli]
        for li in li:       
            m = bfs(2,m,li)
            pos = [i for i in li if m[i] != '0'][0]
            pack = m[pos]
            for i in li:
                if m[i] == pack:
                    fix.append(i)
                else:
                    m = sort(m,None,i,pack)
        # 돌리면서 정렬
        li1,li2 = [3,11,23,27],[2,6,18,26]
        for i in range(1,5):
            m = bfs(3,m,li1,li2,i,0)
        for i in range(1,5):
            m = bfs(3,m,li1,li2,4,i)
    if t == 1:
        pass
    if t == 2:
        pass
    return res

t,m,hli = 0,'xx61xx13xx40x6005x2x02x5xx43xx',[14, 15]
        
ts = time()    
res = main(t,m,hli) if t == 0 else None  
te = time() - ts
if isinstance(res[0],list):
    print(res)
else:
    for i in res:
        printf(i,5,6,hli)
print("{}step, idle {}s(dart {}m {}s) \n".
format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
