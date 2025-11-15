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
    res = []    
    if t == 2:
        dy,dx = [-1,0,1,0,-1,1,1,-1],[0,1,0,-1,1,1,-1,-1]
    else:
        dy,dx = [-1,0,1,0],[0,1,0,-1]
    y,x = divmod(pos,sx)
    for i in range(8):
        ny,nx = y + dy[i],x + dx[i]
        if -1 < ny < sy and -1 < nx < sx:
            res.append(ny * sx + nx)
    cache[pos] = res
    return res

def exp(n,m,pos=-1,p:'t == 2'=-1):
    res = []
    for i in range(size) if n > 0 else [pos]:
        if (n > 0 and m[i] != '0') or i in fix:
            continue
        if t == 2 and n > 0 and i in hli:
            continue
        for j in aro(i):
            d = abs(i - j)
            def b(pos1,pos2,d):
                pack = p if p != -1 else m[pos2]
                if pack in (['0x','x'][t == 2] if n > 0 else 'x') or pos2 in fix:
                    return True
                if t == 2:
                    nd = abs(pos1 - pos2)
                    if d in [4,6] and nd not in [4,6] or \
                       d in [1,5] and nd not in [1,5] or \
                       (pack in '1234' and d in [4,6]) or \
                       (pack in '5678' and d in [1,5]):
                        return True
            if b(i,j,d):
                continue            
            if t == 2 and n > 0:
                if j in hli:
                    li = [j]
                    for hp in li:           # hole position
                        
                        li0 = [li[0]] + ([] if hp == li[0] else [hp])        # 'li' init state coped                        
                        for k in aro(hp):                            
                            if b(hp,k,d) or k in li:
                                continue                            
                            if m[k] == '0':
                                if k in hli:
                                    li.append(k)
                                continue                            
                            res.append(exc(m,i,k,([i]+li0+[k])[::-1]))                            
                if m[j] == '0':
                    continue                
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def bfs(n,m,*a,p:'t == 2'=-1):
    global res
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 2:
        li1,li2 = a
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n == 0 and cur == e:
            break
        if n == 1:
            if (pos == -1 and cur == leaf) or \
               (pos != -1 and cur[pos] == pack):
                break
        if n == 2 and \
           all([cur[i] == '0' for i in li1]) and \
           all([cur[i] != '0' for i in li2]):
            break
        for i,j in exp(n,cur if n > 0 else m,cur,p):
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
    res = []
    pack = leaf[e] if p == -1 else p
    if m[e] == pack:
        fix.append(e)
        return m    
    if pack != '0':
        s = m.index(pack)
        if t == 2:
            fix.remove(e)       # 고정컨
            r = bfs(0,m,s,e,p=pack)
            if not (pack in '5678' and e not in [0,4,20,24,5,9,15,19]):
                fix.append(e)
            r = [i for i in r if i not in hli]            
        for i in r:
            if i in fix:
                fix.remove(i)
            m = bfs(1,m,leaf,i,pack)
    else:
        m = bfs(1,m,leaf,e,'0')
    fix.append(e)
    return m

def main(g_t,m,*a):    
    global t,sy,sx,size,fix,res,cache
    t = g_t
    sy,sx = [[4,4],[4,5],[5,5]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}      # cache reset
    if t == 0:
        pass
    if t == 1:
        pass
    if t == 2:
        global hli
        leaf,hli = a
        hold = []       # 이미 땡긴팩
        unhold = []         # 홀딩 해제 경로
        for pos in range(10):
            fix = [0,1,2,3,4,5,6,7,8,9,10][:pos]

            # 사용할 수 없는 위치
            if (leaf[pos] == '0' and pos == 0 and leaf[1] in '78' and leaf[5] in '78') or \
               (leaf[pos] == '0' and pos == 4 and leaf[3] in '78' and leaf[9] in '78'):
                m = sort(m,leaf,pos,'0')
                continue
            
            if pos in hli :        # 정렬 위치 홀
                continue
            if leaf[pos] == '0' or leaf[pos] in hold:
                li = []
                for i in '12345678':
                    if i not in hold and \
                       i not in (['5','6'] if pos % 2 else ['7','8']) and \
                       m.index(i) not in fix:
                        li.append(i)                
                di = {}
                for i in li:
                    li1 = [j for j in '12345678' if i != j and m.index(j) not in fix]
                    fc = fix[:]
                    fix += [leaf.index(j) for j in li1]                    
                    s = leaf.index(i)
                    try:
                        di[i] = [s]+bfs(0,leaf,s,pos,p = i)
                    except:
                        pass
                    fix = fc[:]
                if not di:
                    continue                    
                pack = min(di,key = lambda n:len(di[n]))
                hold.append(pack)
                unhold.append(di[pack][::-1])
            else:
                pack = leaf[pos]
            if pos < 5:
                li = [0,1,2,3,4,20,21,22,23,24][pos:]
            else:
                li = [0,1,2,3,4,5,6,7,8,9][pos:]
            for i in li:
                m = sort(m,leaf,i,'0')
            m = sort(m,leaf,pos,pack)
            
        li = [i for i in '12345678' if m.index(i) not in fix]
        for i in li:
            e = leaf.index(i)
            m = bfs(1,m,leaf,e,i)
            fix.append(e)
            
        for r in unhold[::-1]:
            if any([m[i] != '0' for i in r[1:]]):
                print(unhold[::-1],'\n->',r)
                exit()                
            m,step = exc(m,r[-1],r[0],r)
            res += step
    return res

if __name__ == '__main__':
    t,m1,m2,a = 2,'0010004800000000002350670','0030005010000800026040070',[16, 10]

    printf(m1,5,5)
    printf(m2,5,5)

    ts = time()    
    res = main(t,m1,m2,a)    
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
