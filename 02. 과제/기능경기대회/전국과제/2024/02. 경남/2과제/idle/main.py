from collections import deque
from time import time
from printer import printf

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    info = [[e,s] if li == -1 else li,int(m[s])]
    return [''.join(m), info]
    
def aro(pos):
    if pos in cache:
        return cache[pos]
    di = [{3:[16,19], 4:[20,23],
           16:[3,32], 19:[3], 20:[4], 23:[4,39],
           32:[16,51], 35:[51], 36:[52], 39:[23,52],
           51:[32,35],52:[36,39]},
          {0:[6], 4:[8],
           6:[0], 8:[4],
           16:[20], 18:[24],
           20:[16], 24:[18]},
           None][t]
    res = di[pos] if pos in di else []
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
    for i in range(size * sz) if n > 0 else [pos]:
        if (n > 0 and m[i] != '0') or i in fix:       # default rule
            continue
        if t == 0 and n > 0 and i in hli:       # A rule
            continue
        for j in range(15) if t == 2 else aro(i):            
            b = lambda j: m[j] in 'x' or j in fix
            if b(j):
                continue
            if t == 0 and n > 0 and j in hli:         # A rule --- 홀 이동 조건
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
                            res.append(exc(m,i,k,li=res1[::-1]))
            if n > 0 and m[j] == '0':       # default rule
                continue     
            if t == 0 and n > 0:      # A - FilteringStep
                for k in res:
                    _,step = k
                    step = step[0]
                    if [j,i] == [step[0],step[-1]]:
                        res.remove(k)
            if t == 1 and n > 0:        # B rule
                if i in red and m[j] not in '123' or i in blue and m[j] not in '4567':
                   continue            
            if t == 2:      # C rule
                if (i > 4 and (m[i - 5] == '0' or i - 5 == j)) or (j < 10 and m[j + 5] != '0'):
                    continue
                if m[j] in '123':       # 1 2 3 pack rule
                    if i not in [[0,1,2,3,4],[5,6,7,8,9],[10,11,12,13,14]][int(m[j])-1]:
                        continue
                    a,b = sorted([i,j])
                    if any([i != '0' for i in m[a+1:b]]):
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
    if n == 4:        # used C
        pack, = a
    cur =  m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n == 0 and cur == e:
            break
        if n == 1:
            cur1 = cur
            if (pos == -1 and cur1 == leaf) or (pos != -1 and cur1[pos] == pack):
                break            
        if n == 2 and [cur[i] for i in li].count('0') < 2:
            break
        if n == 3:
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
        if n == 4:
            pos = cur.index(pack)
            if pos > 9 or cur[pos + 5] == '0':
                break
        for i,j in exp(n,cur if n > 0 else m,cur):
            if i not in mkd:
                que.append(i)
                mkd[i],step[i] = cur,j
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
    global fix
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
    global t,sy,sx,sz,size,fix,res,cache
    t = g_t
    sy,sx,sz = [[7,8,1],[5,5,1],[1,5,3]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}      # cache reset
    if t == 0:
        global hli
        hli, = a
        # 중앙 정렬
        li = [[18,21],[26,29],[27,28]] if m[19] == 'x' else [[34,37],[26,29],[27,28]]
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
        li1,li2 = [3,16,32,51],[4,23,39,52]
        for i in range(1,5):
            m = bfs(3,m,li1,li2,i,0)
        for i in range(1,5):
            m = bfs(3,m,li1,li2,0,i)
    if t == 1:
        global leaf,red,blue        
        leaf,li = a
        red,blue = li
        area = red + blue
    if t == 2:
        leaf, = a
        li = [[4,3,2,1],[0,4,3,2],[0,4,1,3],[4,0,1,2],[0,1,2,3]]
        for pos in li[leaf.index('1')]:
            pack = leaf[pos]
            for i in range(10+pos,pos-1,-5):
                m = bfs(1,m,leaf,i,'0')
            fix.append(pos)
            m = bfs(4,m,pack)
            i,j = pos,m.index(pack)
            m,step = exc(m,i,j)    
            res.append(step)
        fix = [0,1,2,3,4]
        m = bfs(1,m,leaf,-1,-1)
    return res

if __name__ == '__main__':
    # t,m,hli = 0,'xxx35xxxxxxxxxxx6xx46xx1xx4001xx3x2xx0x2xxxxxxxxxxx50xxx',[27, 28]
    # t,m,leaf,li = 1,'xx0x0x614x03x70x25xx0x0x0','xx0x0x123x04x50x67xx0x0x0',[[4, 20], [10, 22]]
    # t,m,leaf =  2,'567180924000300','158970246000300'

    # t,m,hli = 0,'xxx11xxxxxxxxxxx4x2xx3x5xx3002xx5xx06xx4xxxxxxxxxxx60xxx',[27, 28]
    # t,m,leaf,li = 1,'xx0x0x614x03x70x25xx0x0x0','xx0x0x123x04x50x67xx0x0x0',[[4, 20], [10, 22]]
    t,m,leaf = 2,'186470529000300','491670582000300'

                
    ts = time()    
    res = main(t,m,hli) if t == 0 else main(t,m,leaf,li)  if t == 1 else main(t,m,leaf)  
    te = time() - ts
    print(res)
    # if isinstance(res[0],list):
    #     print(res)
    # else:        
    #     for i in res:
    #         if t == 0:
    #             printf(i,7,8,hli) 
    #         if t == 1:
    #             h,m = i
    #             print('Heuristic ->',h)
    #             printf(m,5,5)
    #             printf(leaf,5,5)
    #         if t == 2:
    #             printf(i,1,5,3)
    print("{}step, idle {}s(dart {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
    