from collections import deque
from time import time
from printer import printf

def exc(m,s,e=-1,g=-1,p=-1,gli=-1,li=-1):
    m = list(m)
    if g != -1:
        isg = g == 1
        pack = m[s] if isg else p
        gp = int(pack in '123') if isg else gli.index(p)
        gli = list(gli)
        gli[gp] = pack if isg else '0'
        m[s] = '0' if isg else p
    else:
        m[s],m[e] = m[e],m[s]
        pack = m[s]
        if t == 2:
            gp = int(pack in '123')
    pack = int(pack)
    info = [s,g,pack,gp] if g != -1 else [[e,s] if li == -1 else li,pack]
    if t == 2 and g == -1:
        info.append(gp)
    return [(''.join(m),tuple(gli)) if t == 2 else ''.join(m), info]
    
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
    res = di[pos] if t < 2 and pos in di else []
    dy,dx = [-1,0,1,0]*5,[0,1,0,-1]*5
    dz = [-2]*4 + [-1]*4 + [0]*4 + [1]*4 + [2]*4
    y,x,z = (pos // sx) % sy, pos % sx, pos // size
    for i in range(20):
        ny,nx,nz = y + dy[i],x + dx[i],z + dz[i]
        if -1 < ny < sy and -1 < nx < sx and -1 < nz < sz:
            n = ny * sx + nx + (size * nz)
            res.append(n)
    cache[pos] = res
    return res

def exp(n,m,pos=-1):
    if t == 2:
        m,gli = m
    res = []
    for i in range(size * sz) if n > 0 else [pos]:
        if i in fix:       # default rule       
            continue
        if t == 0 and n > 0 and i in hli:       # A rule
            continue
        if t == 2:      # C rule
            b1 = lambda pos,pack : pack in '123' and pos not in [[0,1,2,3,4],[5,6,7,8,9],[10,11,12,13,14]][int(pack)-1]
            b2 = lambda pack,gli : (pack in '123' and gli[1] != '0') or (pack not in '123' and gli[0] != '0')            
            if m[i] == '0' and gli.count('0') < 2 and (i > 9 or m[i + 5] == '0') and (i < 5 or m[i - 5] != '0'):        # put a pack
                for p in gli:
                    if p == '0' or b1(i,p):
                        continue                   
                    res.append(exc(m,i,g=0,p=p,gli=gli))
            if gli.count('0') < 2:      # used all gripper
                continue
            if m[i] not in '0123' and (i > 9 or m[i + 5] == '0') and not b2(m[i],gli):      # get a pack
                res.append(exc(m,i,g=1,gli=gli))
        if n > 0 and m[i] != '0':       # default rule
            continue
        for j in aro(i):            
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
            if t == 1 and n > 0:        # B rule
                if i in red and m[j] not in '123' or i in blue and m[j] not in '4567':
                   continue            
            if t == 2:      # C rule
                if (i > 4 and m[i - 5] == '0') or (j < 10 and m[j + 5] != '0') or b1(i,m[j]) or b2(m[j],gli):
                    continue
            res.append(exc(m,i,j,gli = gli if t == 2 else -1) if n > 0 else [j,j])
    return res

def bfs(n,m,*a):
    global res
    if n == -1:     # used B
        s,st,li = a
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 2:      # used A
        li, = a
    if n == 3:      # used A
        li1,li2,ct1,ct2 = a

    if n == 101:        # used C
        pos,pack = a

    cur =  m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n == -1:
            pack = m[cur]
            if pack in st and pack not in li:
                break
        if n == 0 and cur == e:
            break
        if n == 1:
            cur1 = cur[0] if t == 2 else cur
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

        if n == 101 and cur[0][pos] == '0' and pack in cur[1]:
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
        printf(m,5,5)
        printf(leaf,5,5)

    if t == 2:
        m = '105672008430009'
        m = (m,('0','0'))
        leaf, = a

        for i,j in exp(1,m):
            print(j)
            print(i[1])
            printf(i[0],1,5,3)


        # li = [[4,3,2,1],
        #       [0,4,3,2],
        #       [0,4,1,3],
        #       [4,0,1,2],
        #       [0,1,2,3]]
        # for pos in li[leaf.index('1')]:
            
        #     print('pos ->',pos,', pack ->',leaf[pos])
            
        #     ts = time()
        #     for i in range(10+(pos%5),pos-1,-5):
        #         m = bfs(1,m,leaf,i,'0')
        #     m = bfs(101,m,pos,leaf[pos])
            
        #     print('Cleared')
        #     printf(m,1,5,3)
        #     m = bfs(1,m,leaf,pos,leaf[pos])
        #     fix.append(pos)

        #     print('in',time() - ts)
        #     printf(m,1,5,3)
            

    return res

if __name__ == '__main__':
    # t,m,hli = 0,'xxx35xxxxxxxxxxx6xx46xx1xx4001xx3x2xx0x2xxxxxxxxxxx50xxx',[27, 28]
    # t,m,leaf,li = 1,'xx0x0x614x03x70x25xx0x0x0','xx0x0x123x04x50x67xx0x0x0',[[4, 20], [10, 22]]
    t,m,leaf =  2,'567180924000300','158970246000300'

    # t,m,hli = 0,'xxx11xxxxxxxxxxx4x2xx3x5xx3002xx5xx06xx4xxxxxxxxxxx60xxx',[27, 28]
    # t,m,leaf,li = 1,'xx0x0x614x03x70x25xx0x0x0','xx0x0x123x04x50x67xx0x0x0',[[4, 20], [10, 22]]
    # t,m,leaf = 2,'186470529000300','491670582000300'
                
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
    #             m,gli = i
    #             print(gli)
    #             printf(m,1,5,3)
    print("{}step, idle {}s(dart {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
    