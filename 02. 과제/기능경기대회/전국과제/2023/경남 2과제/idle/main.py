from collections import deque
from time import time
from printer import printf

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    step = [e,s] if li == -1 else li
    pack = 'abc'.index(m[s])+10 if m[s].isalpha() else int(m[s])
    info = [step,pack]+([ing] if t == 0 else [])
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
def exp(n,m,pos=-1,p=-1):
    res = []
    if t == 0:
        hli1 = hli[ing]
    if t == 1:
        hli1 = hli[:]
    if t == 2:
        hli1 = hli[0]
    for i in range(size) if n > 0 else [pos]:
        if (n > 0 and m[i] != '0') or i in fix:
            continue
        if n > 0 and i in hli1 and (n != 4 or i != pos):
            continue
        for j in aro(i):
            b1 = lambda pos: m[pos] == 'x' or pos in fix
            b2 = lambda pos1,pos2:  n == 4 and pos1 == pos and m[pos2] not in ['0',p]
            if b1(j) or b2(i,j):
                continue
            if n > 0:                
                if j in hli1 and m[j] == '0':
                    que = deque([j])
                    mkd = {j:i,i:-1}
                    while que:
                        cur = que.popleft()
                        for k in aro(cur):
                            if k not in mkd:                                
                                mkd[k] = cur
                                if k in hli1 and m[k] == '0':
                                    que.append(k)
                                if m[k] == '0' or b1(k) or b2(i,k):
                                    continue
                                res1 = path(mkd,mkd,k)+[k]
                                if t == 1:
                                    if (hli1[1] in res1 and m[k] in '789abc') or \
                                       (hli1[2] in res1 and m[k] in '123456'):
                                        continue
                                res.append(exc(m,i,k,res1[::-1]))                        
                if m[j] == '0':
                    continue                
            if t == 1 and n < 1 and p != -1:
                if (p in '123456' and j == hli1[2]) or \
                   (p in '789abc' and j == hli1[1]):
                    continue
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res
def bfs(n,m,*a,p=-1):
    global res
    if n < 1:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 2:
        li,limit = a
        ct = 0
    if n == 3:
        leaf,li = a
    if n == 4:
        hp, = a
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        if n == -1 and not que:
            return -1
        if n == 2:
            if limit != -1 and (ct > limit or not que):
                return -1
            ct += 1
        cur = que.popleft()
        if n < 1 and cur == e:
            break
        if n == 1:
            if (pos == -1 and cur == leaf) or \
               (pos != -1 and cur[pos] == pack):
                break
        b1 = n == 2 and all([cur[i] == '0' for i in li])
        b2 = n == 3 and all([cur[i] == leaf[i] for i in li])
        b3 = n == 4 and cur[hp] == p
        if b1 or b2 or b3:
            break
        for i,j in exp(n,cur if n>0 else m,
                       cur if n < 1 else hp if n == 4 else -1,
                       p if p != -1 else -1):
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
def sort(m,leaf,e,p = -1):
    global fix,res
    pack = leaf[e] if p == -1 else p
    if t == 1:
        ct = 0
        while 1:
            s = m.index(pack)
            r = bfs(0,m,s,e,p = pack)
            if len([i for i in r if i not in hli]) > 4:
                pos1 = r[ct]
                m = sort(m,leaf,pos1,pack)
                fix.remove(pos1)
                ct += 1
                continue
            fix.append(s)
            road = []
            for pos in r[::-1]:
                road.append(pos)
                if m[pos] == '0':
                    continue
                for i in range(2):
                    res1 = bfs(2,m,road if i else ([pos]+road[:-1]),[7000,-1][i])
                    if res1 == -1:
                        fix.remove(s)
                    else:
                        m = res1[:]
                        break
            if s in fix:
                break            
        fix.remove(s)
        m,step = exc(m,e,s,[s]+r)
        res.append(step)        
    else:
        hli1 = hli[ing] if t == 0 else hli[0]
        s = [i for i in range(size) if i not in fix and m[i] == pack][0]
        r = bfs(0,m,s,e)
        if t == 2 and e in hli1:
            r = [i for i in r if i not in hli1 or i == e]
            for i in r:
                m = bfs(4,m,i,p = pack)
        else:
            r = [i for i in r if i not in hli1]
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
    cache = {}
    if t in [0,1]:
        global hli
    if t == 0:
        global ing
        m1 = m[:]
        m2,hli = a
        m1,m2 = map(list,[m1,m2])
        for i in range(15):
            if m1[i] in '456':
                j = [j for j in range(15) if m2[j] in '123'][0]
                m1[i],m2[j] = m2[j],m1[i]
                res.append([i,j,int(m1[i]),int(m2[j])])
        m1,m2 = map(''.join,[m1,m2])
        leaf = []
        for i in range(2):
            m3 = ['0'] * 15
            ct = [-1,0,0,0,0,0,0]
            li = ([j for j in range(15) if leaf[0][j] == '0'] if i else [])+list(range(15)) 
            for j in hli[1-i]+li:
                pack = j // 5 + (3 * i) + 1
                if j not in hli[i] and m3[j] == '0' and ct[pack] < 3:
                    m3[j] = str(pack)
                    ct[pack] += 1
            leaf.append(''.join(m3))
        leaf1,leaf2 = leaf
        for i in range(2):
            ing = i
            m = [m1,m2][i]
            leaf = [leaf1,leaf2][i]            
            for j in range(5):
                if j in hli[i] or leaf[j] == '0':
                    m = bfs(1,m,leaf,j,'0')
                    fix.append(j)
                else:
                    m = sort(m,leaf,j)
            bfs(1,m,leaf,-1,-1)
            fix = []
    if t == 1:
        leaf,hli = a     
        hold = []
        unhold = []
        def getli(li,n):
            li1 = []
            li2 = [i+n in hli[1:] for i in li]
            if (li2[2] and li2[3]) or (li2.count(1) == 1 and li2[2]):
                li1 = li[::-1]
            elif not (li2.count(1) == 1 and li2[1]):
                for i in li:
                    if i+n in hli[1:]:
                        li1.append(i)
            li1 += [i for i in li if i not in li1]
            return li1        
        li = []
        if all([i in [3,4,8,9,13,14,18,19] for i in hli[1:]]):
            for i in [[4,9,14,19],[3,8,13,18],[2,7,12,17]]:
                li += getli(i,-1)
        else:
            for i in [[0,5,10,15],[1,6,11,16],[2,7,12,17]]:
                li += getli(i,1)
        for pos in li:            
            if pos in hli:
                continue
            if leaf[pos] in hold+['0']:
                li1 = []
                for i in range(size):
                    if i not in fix and leaf[i] not in hold+['0']:
                        pack = leaf[i]
                        fc = fix[:]
                        li2 = [leaf.index(j) for j in '123456789abc'
                               if j != pack and m.index(j) not in fix]
                        for j in li2:
                            fix.append(j)
                        r = bfs(-1,leaf,pos,i,p = pack)
                        fix = fc[:]
                        if r != -1:
                            r = [pos]+r
                            li1.append([pack,r])
                pack,r = min(li1,key = lambda n: len(n[1]))
                hold.append(pack)
                unhold.append(r)                
            else:
                pack = leaf[pos]                
            if m[pos] == pack:
                fix.append(pos)
                continue
            m = sort(m,leaf,pos,pack)
        li = [m[i] for i in range(size) if i not in fix and m[i] != '0']
        li = [leaf.index(i) for i in li]
        m = bfs(3,m,leaf,li)
        for r in unhold[::-1]:
            m,step = exc(m,r[-1],r[0],r)
            res.append(step)
    if t == 2:
        leaf,hli = a     
        leaf_copy = leaf[:]
        for i in range(3):
            li,root,leaf = hli[0][:],hli[1][:],hli[2][:]
            if root[i] != leaf[i]:
                j = root.index(leaf[i])
                for k in [i,j]:
                    pos,pack = li[k],str(root[k])
                    if m[pos] != pack:
                        m = sort(m,leaf,pos,pack)
                s,e = li[i],li[j]
                m,step = exc(m,s,e)
                step = [e,s,root[i],root[j]]
                res.append(step)
                root[i],root[j] = root[j],root[i]
                hli[1] = root[:]
                fc = fix[:]
                for k in fc:
                    n = hli[0].index(k)
                    if hli[1][n] == hli[2][n]:
                        fix.remove(k)             
                m = bfs(2,m,[k for k in [s, e] if k not in fix],-1)                
        leaf = leaf_copy[:]
        hold = []
        for i in [0,4,8,1,5,9,2,6,10]:
            if i in hli[0]:
                continue
            if leaf[i] in hold+['0']:
                di = {}
                y1,x1 = divmod(i,4)
                for j in '123456':
                    if m.index(j) not in fix and j not in hold:
                        y2,x2 = divmod(leaf.index(j),4)
                        di[j] = abs(y1 - y2) + abs(x1 - x2)
                if not di:
                    break
                pack = min(di,key = lambda n:di[n])
                hold.append(pack)
            else:
                pack = leaf[i]
            m = sort(m,leaf,i,pack)
        for i in hold[::-1]:
            s,e = m.index(i),leaf.index(i)
            fix.remove(s)
            m = bfs(1,m,leaf,e,i)
            fix.append(e)
    return res

if __name__ == '__main__':

    # DART    
##    t,m1,m2,a = 0,'051002426053060','510642030314000',[[0, 9, 14], [2, 6, 12]]
##    t,m1,m2,a = 1,'0ab971c2800030500640','00310098c204b0a07560',[15, 13, 19]
##    t,m1,m2,a = 2,'006041302500','030021645000',[[10, 0, 3], [5, 4, 2], [5, 2, 4]]

    # IDLE
##    t,m1,m2,a = 0,'43013''01025''30040','60266''01504''00502',[[2, 7, 12], [1, 8, 11]]
    t,m1,m2,a = 1,'605a0709038400c0b201','60c50903a0020871040b',[4, 6, 12]
##    t,m1,m2,a = 2,'014530060020','032004006015',[[0, 6, 9], [4, 5, 1], [1, 4, 5]]
    
    ts = time() 
    res = main(t,m1,m2,a)
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,6),int((te*250)//60),int((te*250)%60)))
