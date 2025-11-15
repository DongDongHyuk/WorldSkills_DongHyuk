from collections import deque
from time import time
from printer import printf

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    step = [e,s] if li == -1 else li
    pack = 'abc'.index(m[s])+10 if m[s].isalpha() else int(m[s])
    info = ([ing] if t == 0 else [])+[step,pack]
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
    if t == 0:
        hli0 = hli[ing]
    for i in range(size) if n > 0 else [pos]:       
        if (n > 0 and m[i] != '0') or i in fix:
            continue
        if t == 0 and n > 0 and i in hli0:
            continue
        for j in aro(i):
            b = lambda pos: \
                m[pos] not in (['0x','x'][t == 0] if n > 0 else 'x') and pos not in fix
            if not b(j):
                continue
            if t == 0 and n > 0:                
                if j in hli0:
                    li = [j]
                    for hp in li:           # hole position
                        li0 = [li[0]] + ([] if hp == li[0] else [hp])        # 'li' init state coped                        
                        for k in aro(hp):
                            if not b(k) or k in li:
                                continue
                            if m[k] == '0':
                                if k in hli0:
                                    li.append(k)
                                continue                                
                            res.append(exc(m,i,k,([i]+li0+[k])[::-1]))                        
                if m[j] == '0':
                    continue
            if t == 1 and n == -1 and m[j] != '0':
                continue
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def exp0(*m):
    global fix
    res = []
    m = m[1]
    for i in range(size):
        pack = m[i]
        if pack == '0' or i in fix:
            continue
        fc = fix[:]
        fix.append(hli[2 if pack in '123456' else 1])
        mkd,step = bfs(-1,m,i)
        for j in mkd:
            if j not in fix+hli+[i]:
                r = [i]+path(mkd,step,j)
                res.append(exc(m,j,i,r))        
        fix = fc[:]        
    return res

def bfs(n,m,*a):
    global res,fix
    if n == -2:
        leaf,s,li = a
    if n == -1:
        s, = a
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 2:
        li,pack = a
    if n == 3:
        li,pack = a
    expand = exp0 if t == 1 and n > 0 else exp
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        if n == -2:
            pack = leaf[cur]
            if pack != '0' and cur not in li:
                fc = fix[:]
                fix.append(hli[2 if pack in '123456' else 1])
                r = bfs(0,leaf,s,cur)
                fix = fc[:]
                y1,x1 = divmod(s,5)
                y2,x2 = divmod(cur,5)
                if abs(y1 - y2) + abs(x1 - x2) == len(r):
                    break
        if n == -1 and not que:
            return mkd,step
        cur = que.popleft()
        if n == 0 and cur == e:
            break
        if n == 1:
            if (pos == -1 and cur == leaf) or \
               (pos != -1 and cur[pos] == pack):
                break
        if n == 2:
            li = [i for i in li if i not in fix + hli]
            if not [i for i in li if cur[i] == '0'] and \
               pack not in [cur[i] for i in li]:
                break
        if n == 3 and pack in [cur[i] for i in li]:
            break
        for i,j in expand(n,cur if n > 0 else m,cur):
            if i not in mkd:
                que.append(i)
                mkd[i],step[i] = cur,j
    mkd[-2] = cur
    res0 = path(mkd,step)
    if n > 0 :
        res += res0
        return mkd[-2]
    return res0
    
def path(mkd,step,cur = -1):
    cur = mkd[-2] if cur == -1 else cur
    path = [step[cur]]
    while mkd[cur] != -1:
        cur = mkd[cur]
        path.append(step[cur])
    return path[::-1][1:]
        
def sort(m,leaf,e):
    global fix
    res = []
    pack = leaf[e]
    s = [i for i in range(size) if i not in fix and m[i] == pack][0]
    r = bfs(0,m,s,e)
    if t == 0:
        r = [i for i in r if i not in hli[ing]]
    for i in r:
        m = bfs(1,m,leaf,i,pack)
    fix.append(e)
    return m

def main(g_t,m,*a):    
    global t,sy,sx,size,fix,res,cache
    t = g_t
    sy,sx = [[3,5],[4,5],[3,4]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}      # cache reset
    if t in [0,1]:
        global hli
    if t == 0:
        global ing
        m1 = m[:]
        m2,hli = a
        m1,m2 = map(list,[m1,m2])       # pack exchanging
        for i in range(15):
            if m1[i] in '456':
                j = [j for j in range(15) if m2[j] in '123'][0]
                m1[i],m2[j] = m2[j],m1[i]
                res.append([i,j,m1[i],m2[j]])
        m1,m2 = map(''.join,[m1,m2])
        leaf = []       # making leaf
        for i in range(2):
            m0 = ['0'] * 15
            ct = [-1,0,0,0,0,0,0]
            li = ([j for j in range(15) if leaf[0][j] == '0'] if i else [])+list(range(15)) 
            for j in hli[1-i]+li:
                pack = j // 5 + (3 * i) + 1
                if j not in hli[i] and m0[j] == '0' and ct[pack] < 3:
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
                else:
                    m = sort(m,leaf,j)
            m = bfs(1,m,leaf,-1,-1)
            if i:
                m2 = m[:]
            else:
                m1 = m[:]
            fix = []        # fix reset
    if t == 1:
        leaf,hli = a

        def getli(li,n):
            li1 = []
            li2 = hli[1:]
            if all([i+n in li2 for i in li[2:]]):
                li1 = li[::-1]
            else:
                for i in li:
                    if i+n in li2:
                        li1.append(i)
            li1 += [i for i in li if i not in li1]
            return li1

        sli = getli([0,5,10,15],1)
        
        hold = []
        unhold = []
        for ct,pos in enumerate(sli):
            if pos in hli:
                continue
            # 정렬 할 팩
            if leaf[pos] is '0' or pos in hold:
                r = bfs(-2,m,leaf,pos,hold)
                pos1 = r[-1]
                pack = leaf[pos1]
                hold.append(pos1)
                unhold += [r+[pos]]
            else:
                pack = leaf[pos]

            vt = [0,4,15,19]
            s = m.index(pack)
            if s in vt:
                m = bfs(1,m,leaf,s,'0')
                printf(m,4,5)
                fix.append(s)
            
            m = bfs(3,m,[6,7,8,11,12,13],pack)
            printf(m,4,5)

            break

            

        
                
    if t == 2:
        pass
    
    return res

if __name__ == '__main__':
    
##    t,m1,m2,a = 0,'051002426053060','510642030314000',[[0, 9, 14], [2, 6, 12]]
    t,m1,m2,a = 1,'090004200b78a001356c','0b3501006a9c08720004',[0, 4, 7]

##    printf(m1,4,5)
##    printf(m2,4,5)
        
    ts = time() 
    res = main(t,m1,m2,a)
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,6),int((te*250)//60),int((te*250)%60)))
