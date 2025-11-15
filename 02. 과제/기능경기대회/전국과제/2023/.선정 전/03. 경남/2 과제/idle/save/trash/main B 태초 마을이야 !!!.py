from collections import deque
from time import time
from printer import printf

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    step = [e,s] if li is -1 else li
    pack = 'abc'.index(m[s])+10 if m[s].isalpha() else int(m[s])
    info = ([ing] if t is 0 else [])+[step,pack]
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
    if t is 0:
        hli0 = hli[ing]
    if t is 1:
        hli0 = hli[:]
    for i in range(size) if n > 0 else [pos]:       
        if (n > 0 and m[i] != '0') or i in fix:
            continue
        if t < 2 and n > 0 and i in hli0:
            continue
        for j in aro(i):
            b = lambda pos: \
                m[pos] not in (['0x','x'][t < 2] if n > 0 else 'x') and pos not in fix
            if not b(j):
                continue
            if t < 2 and n > 0:
                
                if j in hli0:
                    li = [j]
                    for hp in li:           # hole position
                        li0 = [li[0]] + ([] if hp is li[0] else [hp])        # 'li' init state coped                        
                        for k in aro(hp):
                            if not b(k) or k in li:
                                continue                            
                            if m[k] is '0':
                                if k in hli0:
                                    li.append(k)
                                continue
                            if t is 1:
                                if (hli0[1] in li0 and m[k] in '789abc') or \
                                   (hli0[2] in li0 and m[k] in '123456'):
                                    continue                                   
                            res.append(exc(m,i,k,([i]+li0+[k])[::-1]))                        
                if m[j] is '0':
                    continue
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def bfs(n,m,*a):
    global res
    if n is -1:         # 정렬 값이 존재하는 위치 찾기
        leaf,s,li = a
    if n is 0:
        s,e = a
    if n is 1:
        leaf,pos,pack = a
    if n is 2:
        li1,li2,pack = a
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n is -1:
            m0 = leaf if leaf is not -1 else m
            if m0[cur] is not '0' and cur not in li:
               break
        if n is 0 and cur is e:
            break
        if n is 1:
            if (pos is -1 and cur == leaf) or \
               (pos is not -1 and cur[pos] is pack):
                break
        if n is 2:
            if not [i for i in li1 if cur[i] is not '0'] and \
               not [i for i in li2 if cur[i] is '0'] and \
               pack not in [cur[i] for i in li2]:
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
    global fix
    res = []
    pack = leaf[e] if p is -1 else p
    s = [i for i in range(size) if i not in fix and m[i] is pack][0]
    r = bfs(0,m,s,e)        
    if t is 0:
        r = [i for i in r if i not in (hli if t else hli[ing])]         # 홀은 길에서 제외    
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
    if t is 0:
        global ing
        m1 = m[:]
        m2,hli = a
        # pack exchanging
        m1,m2 = map(list,[m1,m2])        
        for i in range(15):
            if m1[i] in '456':
                j = [j for j in range(15) if m2[j] in '123'][0]
                m1[i],m2[j] = m2[j],m1[i]
                res.append([i,j,m1[i],m2[j]])
        m1,m2 = map(''.join,[m1,m2])
        # make leaf
        leaf = []
        for i in range(2):
            m0 = ['0'] * 15
            ct = [-1,0,0,0,0,0,0]
            li = ([j for j in range(15) if leaf[0][j] is '0'] if i else [])+list(range(15)) 
            for j in hli[1-i]+li:
                pack = j // 5 + (3 * i) + 1
                if j not in hli[i] and m0[j] is '0' and ct[pack] < 3:
                    m0[j] = str(pack)
                    ct[pack] += 1
            leaf.append(''.join(m0))
        leaf1,leaf2 = leaf
        for i in range(2):
            ing = i         # now sorting
            m = [m1,m2][i]
            leaf = [leaf1,leaf2][i]            
            for j in [0,1,2,3,4]:
                if j in hli[i] or leaf[j] is '0':
                    m = bfs(1,m,leaf,j,'0')
                    fix.append(j)
                    pass
                else:
                    m = sort(m,leaf,j)
            m = bfs(1,m,leaf,-1,-1)
            if i:
                m2 = m[:]
            else:
                m1 = m[:]
            fix = []        # fix reset
    if t is 1:
        leaf,hli = a
        def getli(li,n):
            li1 = []
            h = hli[1:]
            if all([i+n in h for i in li[2:]]):
                li1 += [i for i in li[2:]][::-1]
            else:
                for i in li:
                    if i+n in h:
                        li1.append(i)
            li1 += [i for i in li if i not in li1]
            li1 = [i for i in li1 if i not in hli]
            return li1
        
        hold = {}
        b = len([i for i in [0,1,2,5,6,7,10,11,12,15,16,17] if i in hli]) >= 2
        
        if not b:
            sli = getli([0,5,10,15],1)      # 정렬 순서
            fli = getli([4,9,14,19],-1)         # 고정 순서 1
            fli += getli([3,8,13,18],-1)        # 고정 순서 2
        else:
            sli = getli([4,9,14,19],-1)      # 정렬 순서
            fli = getli([0,5,10,15],1)         # 고정 순서 1
            fli += getli([1,6,11,16],1)        # 고정 순서 2
            
        for ct,pos in enumerate(sli):
            fix = sli[:ct]
            
            # 정렬 팩
            if leaf[pos] is '0' or pos in hold:         # 정렬 값이 없는 위치거나 다른데서 홀딩인 위치일때
                pos1 = bfs(-1,m,leaf,pos,hold)[-1]
                pack = leaf[pos1]
                hold[pos1] = pos
            else:
                pack = leaf[pos]
            if m[pos] is pack:      # 이미 정렬된 위치일때 컨티뉴
                continue
            
            for i in fli:       # fli -> 고정할 순서
                m = bfs(2,m,[],[i],pack)
                fix.append(i)
                
            m = bfs(1,m,leaf,pos,pack)

##        print(sli,'sorted !!!')
##        printf(m,4,5)
##        printf(leaf,4,5)
    
    if t is 2:
        pass
    return res

if __name__ == '__main__':
    
##    Type,m1,m2,a = 0,'051002426053060','510642030314000',[[0, 9, 14], [2, 6, 12]]
    Type,m1,m2,a = 1,'40830ab0c00912006075','30506a0048c9700b1002',[14, 7, 17]
    
        
    ts = time() 
    res = main(Type,m1,m2,a)    
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
