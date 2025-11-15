from collections import deque
from time import time
from printer import printf

def exc(m,s,e):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    step = [e,s,int(m[s])]
    return [''.join(m),step]
    
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

def exp(n,m,pos=-1):
    res = []
    for i in range(size) if n else [pos]:       
        if (n and m[i] != '0') or i in fix:
            continue
        b = lambda pos: m[pos] not in ['x','0x'][n > 0] and pos not in fix
        for j in [j for j in aro(i) if b(j)]:
            if t is 0:
               if (abs(i-j) is 7 and i < 8) or \
                   (j < 8 and i not in [8,15]) or \
                   (i < 8 and j not in [8,15]):
                    continue
            if t is 2 and n:
                pass
                li = [m[k] for k in hp]
                if li != ['0','0'] and j not in hp:
                   continue
            res.append(exc(m,i,j) if n else [j,j])
    return res

def bfs(n,m,*a):
    global res
    if n is 0:
        s,e = a
    if n is 1:
        leaf,pos,pack = a
    if n is 2:
        leaf,li,li0,n0 = a
    cur = m if n else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n is 0 and cur == e:
            break
        if n is 1:
            if cur == leaf or \
               (pos != -1 and cur[pos] == pack) and \
               (t is not 2 or [cur[i] for i in hp] == ['0','0']):
                break
        if n is 2:
            li1 = ''.join([cur[i] for i in li if cur[i] is not '0'])
            if li0[:n0] in li1:
                break
        for i,j in exp(n,cur if n else m,cur):
            if i not in mkd:
                que.append(i)
                mkd[i],step[i] = cur,j
    mkd[-2] = cur
    path = [step[cur]]
    while mkd[cur] != -1:
        cur = mkd[cur]
        path.append(step[cur])
    if n:
        res += path[::-1][1:]
        return mkd[-2]
    return path[::-1][1:]
    
def sort(m,leaf,e,p=-1):
    pack = leaf[e] if p is -1 else p
    res = []
    s = m.index(pack)

    
    hold = -1
    b = t is 2 and s is not e and len(exp(0,m,e)) is 1
    if b:
        m = bfs(1,m,leaf,e,'0')
        hold = e
    r = bfs(0,m,s,e)
    if t is 2:
        r = [i for i in r if i not in hp]
    if b:
        fix.append(e)
        
    for i in r:
        if i is hold:
            fix.remove(i)
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
    cache = {}      # cache reset
    if t == 0:
        leaf,_ = a
        for i in range(2):
            p = leaf[8+i]
            m = sort(m,leaf,[0,2,5,7][i],p)
        for i in range(4):
            m = sort(m,leaf,11-i,leaf[15-i])
        fix = []
        for i in range(8):
            m = sort(m,leaf,15-i)
        m = sort(m,leaf,12)        
    if t == 1:
        leaf,_ = a
        hold = {}
        li = {2:7,14:13,22:17,10:11}
        for i in li:
            if m[i] is not 'x' and len(fix) < 2:
                m = sort(m,leaf,i,leaf[li[i]])
                hold[li[i]] = i                
        li = [6,7,8,13,18,17]
        li0 = ''.join([leaf[i] for i in li if i not in hold])
        for i in range(1,7):
            m = bfs(2,m,leaf,li,li0,i)
        for i in li:
            if i in hold:
                fix.remove(hold[i])
            m = bfs(1,m,leaf,i,leaf[i])
        printf(m,5,5)
        printf(leaf,5,5)
    if t == 2:
        global hp
        leaf,hp = a

##        print('hp ->',hp)
##        print('root')
##        printf(m,4,4)
##        print('leaf')
##        printf(leaf,4,4)

        m = sort(m,leaf,0)
        
    return res

if __name__ == '__main__':
    
##    Type,root,leaf= 0,'6x0xx0x870453120','0x0xx0x015286743'
    Type,root,leaf = 1,'xx0xxx867x01x20x543xxxxxx','xx0xxx764xx2x10x358xxxxxx'
##    Type,root,leaf,a = 2,'0123x0x06800x054','0500x0x16280x034',[13, 11]

    ts = time()    
    res = main(Type,root,leaf,a if Type is 2 else -1)    
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
