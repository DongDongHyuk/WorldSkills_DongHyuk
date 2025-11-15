from collections import deque
from time import time
from printer import printf

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    step = [e,s] if li == -1 else li
    pack = 'abc'.index(m[s])+10 if m[s].isalpha() else int(m[s])
    info = [step,pack]
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
    for i in range(10 if t == 2 else size) if n > 0 else [pos]:
        if t == 2:
            ct = 1+i
            for j in range(9-i):
                m1 = m[:]
                res1 = []
                for k in range(ct):
                    for l in range(0,20,10):
                        if m[j+k+l] != '0':
                            pos1 = j+k+l
                        if m[ct-k+j+l] != '0':
                             pos2 = ct-k+j+l
                    pos3,pos4 = pos2,pos1
                    if (pos1 < 10 and pos2 < 10) or (pos1 > 9 and pos2 > 9):
                        pos3 = pos2+10 if pos1 < 10 else pos2-10
                        pos4 = pos1+10 if pos1 < 10 else pos1-10
                    if pos1 == pos2:
                        res.append([exc(m1,pos3,pos1)[0]]+[res1+[exc(m,pos3,pos1)[1]]])
                    else:
                        m1 = exc(m,pos3,pos1)[0]
                        m1 = exc(m1 if ct > 2 or (ct == 1 and pos2 != pos3) else m,pos4,pos2)[0]
                        res1 += [exc(m,pos3,pos1)[1]]
                        res1 += [exc(m,pos4,pos2)[1]]
                        if ct in [3,5,7,9] and k-ct == 0 or ct == 1:
                            res.append([m1]+[res1])
                            break
            if i == 9:
                return res
            continue
        if (n > 0 and m[i] != '0') or i in fix:
            continue
        if t == 1 and (m[i] != '0' or \
                       (i > 2 and m[i-3] == '0')):
            continue
        if t == 1:
            li = []
            for x in range(3):
                for z in range(4):
                    pos = z * 3 + x
                    if m[pos] == '0' or \
                       (z != 3 and (pos + 3 == i or m[pos+3] != '0')):
                        continue
                    li.append(pos)
                    break
        for j in [j for j in (li if t == 1 else aro(i))
                  if m[j] not in ['x','0x'][n > 0] and j not in fix]:
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def bfs(n,m,*a):
    global res
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 2:
        li,pack = a
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
        if n == 2:
            li1 = [cur[i] for i in li]
            if pack in li1:
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
    res = []
    pack = leaf[e] if p == -1 else p
    if pack != '0':
        s = m.index(pack)
        r = bfs(0,m,s,e)
        for i in r:
            m = bfs(1,m,leaf,i,pack)
    else:
        m = bfs(1,m,leaf,e,'0')
    fix.append(e)
    return m

def main(g_t,m,*a):    
    global t,sy,sx,size,fix,res,cache
    t = g_t
    sy,sx = [[4,4],[4,3],[0,0]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}      # cache reset
    if t == 0:
        pass
    if t == 1:
        leaf,pack = a
        pos = m.index(pack)
        li = [i for i in range(9)]
        li1 = [pos+i for i in range(3,12,3) if pos+i < 12]
        for i in li1[::-1]:
            if m[i] != '0':
                m = bfs(1,m,leaf,i,'0')
                printf(m,4,3)
        m = list(m)
        m[pos] = '0'
        m = ''.join(m)
        res.append([[-1,pos], int(pack)])
        pos = leaf.index(pack)
        li1 = [pos]+[pos+i for i in range(3,12,3) if pos+i < 12]
        li = [i for i in li if i not in li1]
        for i in li:
            if leaf[i] != '0':
                pack_line = [j+i for j in range(0,12,3)]
                floor = [j for j in [9,10,11] if j not in pack_line]
                m = bfs(2,m,floor,leaf[i])
                fix.append(m.index(leaf[i]))
                m = bfs(2,m,[i],'0')
                fix.remove(m.index(leaf[i]))
                m = bfs(1,m,leaf,i,leaf[i])
                fix.append(i)
        m = bfs(2,m,[leaf.index(pack)],'0')
        m = list(m)
        m[leaf.index(pack)] = pack
        m = ''.join(m)
        res.append([[99,pos], int(pack)])
        m = bfs(1,m,leaf,-1,-1)
    if t == 2:
        leaf, = a
        printf(m,2,10)
        for i,j in exp(1,m):
            print(j)
            printf(i,2,10)
    return res

if __name__ == '__main__':

##    t,m,m1,pack = 1,'756349208001','613572849000','9'
    t,m,m1 = 2,'0705006809a030210040','120406070900508030a0'
    
    ts = time()    
    res = main(t,m,m1)    
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
