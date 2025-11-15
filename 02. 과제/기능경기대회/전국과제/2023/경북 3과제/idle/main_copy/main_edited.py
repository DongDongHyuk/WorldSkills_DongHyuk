from collections import deque
from time import time
from printer import printf

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    step = [e,s] if li == -1 else li
    return [''.join(m),[step,int(m[s])]]
def aro(pos):
    if pos in cache:
        return cache[pos]
    res = []
    if t:
        dy,dx = [-1,0,1,0],[0,1,0,-1]
    else:
        dy = [-1]*15+[0,0]+[1]*15+[0,0]
        dx = list(range(-7,8))+[1,7]+list(range(-7,8))+[-1,-7]
    y,x = divmod(pos,sx)
    for i in range(len(dy)):
        ny,nx = y + dy[i],x + dx[i]
        if -1 < ny < sy and -1 < nx < sx:
            res.append(ny * sx + nx)
    cache[pos] = res
    return res
def exp(n,m,pos=-1,pack=-1):
    res = []
    for i in range(size) if n > 0 else [pos]:       
        if (n > 0 and m[i] != '0') or i in fix:
            continue
        if t == 2 and n > 0 and i in hli:
            continue        
        for j in aro(i):
            b1 = lambda i: m[i] in (['0x','x'][t == 2] if n > 0 else 'x') or i in fix
            b2 = lambda i,j: n == 2 and i == pos and m[j] not in ['0',pack]
            if b1(j) or b2(i,j):
                continue
            if t == 0:
               if (abs(i-j) == 7 and i < 8) or \
                   (j < 8 and i not in [8,15]) or (i < 8 and j not in [8,15]):
                    continue
            if t == 2 and n > 0:
                if j in hli:
                    que = deque([j])
                    mkd = {j:i,i:-1}
                    while que:
                        cur = que.popleft()
                        for k in aro(cur):
                            if k not in mkd:
                                mkd[k] = cur
                                if k in hli:
                                    que.append(k)
                                if m[k] == '0' or b1(k) or b2(i,k):
                                	continue
                                res1 = path(mkd,mkd,k)+[k]
                                res.append(exc(m,i,k,res1[::-1]))
                if m[j] == '0':
                    continue
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res
def bfs(n,m,*a):
    global res    
    if n == -1:
        leaf,s,li = a 
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n in [2,3]:
        pos,pack = a
    if n == 4:
        li1,li2 = a        
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n == -1 and leaf[cur] != '0' and cur not in li:
            break
        if n == 0 and cur == e:
            break
        if n in [1,2]:
            if (pos == -1 and cur == leaf) or\
               (pos != -1 and cur[pos] == pack):
                break
        if n == 3 and cur[pos] not in ['0',pack]:
            break
        if n == 4 and [cur[i] for i in li1] == li2:
            break
        for i,j in exp(n,cur if n > 0 else m,
                       cur if n < 1 else pos if n == 2 else -1,
                       pack if n == 2 else -1):
            if i not in mkd:
                que.append(i)
                mkd[i],step[i] = cur,j                
    res1 = path(mkd,step,cur)    
    if n > 0 :
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
    s = m.index(pack)
    r = bfs(0,m,s,e)
    if t == 2:
        r = [i for i in r if i not in hli]        
    for i in r:
        m = bfs(1,m,leaf,i,pack)
    fix.append(e)
    return m
def main(g_t,m,*a):    
    global t,sy,sx,size,fix,res,cache
    t = g_t
    sy,sx = [[2,8],[5,5],[4,4]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}
    if t == 0:
        leaf, = a
        for i in range(2):
            m = sort(m,leaf,[0,2][i],leaf[8+i])
        for i in [11,12]:
            m = bfs(1,m,leaf,i,'0')
            fix.append(i)
        fix = fix[:-2]        
        for i in range(4):
            m = sort(m,leaf,11-i,leaf[15-i])
        for i in range(4):
            m = bfs(1,m,leaf,12+i,'0')
            fix.append(12+i)
        for i in range(2):
            fix = [] if i else [0,2,5,7]
            for j in range(4):
                m = sort(m,leaf,[15,11][i]-j)
    if t == 1:
        leaf, = a
        li = [2,10,14,22]
        di = {2:7,10:11,14:13,22:17}
        hold = {}
        for i in range(2):
            fix = [hold[j] for j in hold]
            pos = [j for j in li if j not in fix and m[j] != 'x'][0]
            pack = leaf[di[pos]]
            for j in li:
                if j not in fix+[pos]:
                    m = bfs(3,m,j,pack)
                    fix.append(j)
            m = bfs(2,m,pos,pack)
            hold[di[pos]] = pos
            fix = [hold[j] for j in hold]            
        inli = [7,8,13,18,17,16,11,6]
        pos1 = [i for i in li if i not in fix and m[i] != 'x'][0]
        pos = [i for i,j in exp(0,m,pos1) if i in inli][0]
        pos3,pos2 = [inli[(inli.index(pos)-i)%8] for i in range(2)]
        m = bfs(1,m,leaf,pos1,'0')
        leafli = [leaf[i] for i in inli if i not in hold and leaf[i] != '0']
        n = leafli.index(m[pos3])
        leafli = [leafli[(n + i) % 6] for i in range(6)]    
        for pack in leafli:
            curli = [m[i] for i in inli if m[i] in leafli]
            n = leafli.index(pack)-1
            bpack = leafli[n % len(curli)]
            n = curli.index(pack)-1
            if curli[n % len(curli)] == bpack:
                continue
            m = bfs(2,m,pos1,pack)
            for i in range(2):
                edit = fix.remove if i else fix.append
                edit(pos1)
                m = bfs(1,m,leaf,[pos2,pos3][i],[bpack,pack][i])
                edit(pos2)  
        fix = li[:]        
        for i in inli[::-1]:
            if i not in hold and leaf[i] != '0':
                m = bfs(1,m,leaf,i,leaf[i])
                fix.append(i)
        fix = []
        bfs(1,m,leaf,-1,-1)
    if t == 2:
        global hli
        leaf,hli = a        
        hold = {}
        xli = [i for i in range(16) if m[i] == 'x']
        pos = [i for i in [5,6,9,10] if i in xli]
        vt = {5:15,6:12,9:3,10:0}
        if pos:
            pos = pos[0]
            outli = {5:[3,12,7,13,15,14,11], 6:[0,15,4,14,12,13,8], 9:[0,15,1,11,3,2,7], 10:[3,12,2,8,0,1,4]}[pos]
            inli = {5:[1,2,6,10,9,8,4,0], 6:[2,3,7,11,10,9,5,1], 9:[5,6,10,14,13,12,8,4], 10:[6,7,11,15,14,13,9,5]}[pos]
            b = lambda n:n not in hli and n !=vt[pos] and m[n] != 'x'
            pos1 = [i for i in outli if leaf[i] == '0' and b(i)]
            pos1 = pos1[0] if pos1 else [i for i in outli if b(i)][0]
            for i in outli:
                if i not in hli+[pos1] and m[i] !='x':
                    if i in hold or leaf[i] == '0':
                        pos2 = bfs(-1,m,leaf,i,hold)[-1]
                        m = sort(m,leaf,i,leaf[pos2])
                        hold[pos2] = i
                    else:
                        m = sort(m,leaf,i)
            m = bfs(1,m,leaf,pos1,'0')
            leafli = [leaf[i] for i in inli if i not in hold and leaf[i] != '0']
            for pack in leafli:
                curli = [m[i] for i in inli if m[i] in leafli]
                n = leafli.index(pack)-1
                bpack = leafli[n % len(curli)]                
                n = curli.index(pack)-1                
                if curli[n % len(curli)] == bpack:
                    continue                
                m = bfs(2,m,pos1,pack)
                pos = [i for i,j in exp(0,m,pos1) if i in inli][0]
                n = inli.index(pos)
                res1 = []
                for i in range(2):
                    li = [inli[(n + [-j,j][i]) % 8] for j in range(8)]
                    res1.append([j for j in li[1-i:] if j not in hli][0])                    
                pos2,pos3 = res1
                for i in range(2):
                    edit = fix.remove if i else fix.append
                    edit(pos1)
                    m = bfs(1,m,leaf,[pos2,pos3][i],[bpack,pack][i])
                    edit(pos2)                    
            if pos1 in hold:
                fix.remove(hold[pos1])
            m = bfs(2,m,pos1,leaf[pos1])
            fix.append(pos1)
            if pos1 in hold:
                fix.append(hold[pos1])
            for i in inli:
                if i not in hold and leaf[i] != '0':
                    m = bfs(1,m,leaf,i,leaf[i])
                    fix.append(i)
            fix = []
            bfs(1,m,leaf,-1,-1)            
        else:
            unhold = []
            for i in [[0,1,4,3,7,12,13],[3,2,7,0,4,15,14],[12,13,8,0,1,15,11],[15,14,11,3,2,12,8]]:
                if 'x' not in [leaf[j] for j in i[:3]]:
                    li1 = i
            ct = 0
            for i in li1:
                if i not in hli and m[i] != 'x' and ct < 4:
                    if i in hold or leaf[i] == '0':
                        pos = bfs(-1,m,leaf,i,hold)[-1]
                        m = sort(m,leaf,i,leaf[pos])
                        hold[pos] = i
                        unhold.append(pos)
                    else:
                        m = sort(m,leaf,i)
                    ct += 1            
            li1 = [i for i in range(16) if i not in fix and i not in hold]
            li2 = [leaf[i] for i in li1]         
            m = bfs(4,m,li1,li2)
            for i in unhold[::-1]:
                fix.remove(hold[i])
                m = bfs(1,m,leaf,i,leaf[i])
                fix.append(i)            
    return res

if __name__ == '__main__':

    # IDLE 
##    t,r,l = 0,'6x0xx0x870453120','0x0xx0x015286743'
##    t,r,l = 1,'xx0xxx867x01x20x543xxxxxx','xx0xxx764x02x10x358xxxxxx'
##    t,r,l,a = 2,'51x73006208x0x04','06x04000513x8x27',[5, 6]

    # DART
##    t,r,l = 0,'6x3xx8x071450200','0x0xx0x025467813'
##    t,r,l = 1,'xx0xxx160x32x50x487xxxxxx','xx0xxx256x04x30x871xxxxxx'
##    t,r,l,a = 2,'380x0x56720100x4','078x3x10450200x6',[13, 12]
    
    ts = time()
    if t == 2:
        res = main(t,r,l,a)
    else:
        res = main(t,r,l)
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
