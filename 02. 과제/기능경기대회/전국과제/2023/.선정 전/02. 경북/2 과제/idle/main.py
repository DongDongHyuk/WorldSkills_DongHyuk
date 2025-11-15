from collections import deque
from time import time
from printer import printf

def exc(m,s,e):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    return [''.join(m),[e,s]]
    
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
    for i in range(size) if n > 0 else [pos]:       
        if (n > 0 and m[i] != '0') or i in fix:
            continue
        for j in [j for j in aro(i)
                  if m[j] not in ('0x' if n > 0 else 'x') and j not in fix]:
            # A 파레트 - 중앙은 라인을 통해서만 팩이동 가능
            if t is 0 and 7 in [i,j] and line not in [i,j]:
                continue
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def bfs(n,m,*a):
    global res
    if n is -1:
        leaf,s = a 
    if n is 0:
        s,e = a
    if n is 1:
        leaf,pos,pack = a
    if n is 2:
        leaf,li,li0,n0 = a
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n is -1 and \
           leaf[cur] is not '0' and cur not in hold:
            break
        if n is 0 and cur is e:
            break
        if n is 1:
            if cur == leaf or \
                (pos is not -1 and cur[pos] == pack):
                    break
        if n is 2:
            li1 = ''.join([cur[i] for i in li if cur[i] is not '0'])
            if li0[:n0] in li1:
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
    pack = leaf[e] if p is -1 else p
    res = []
    s = m.index(pack)
    r = bfs(0,m,s,e)
    for i in r:
        m = bfs(1,m,leaf,i,pack)
    fix.append(e)
    return m

def main(g_t,m,*a):    
    global t,sy,sx,size,fix,res,cache
    t = g_t
    sy,sx = [[5,3],[3,4],[4,4]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}      # cache reset
    if t is 0:
        global line
        n, = a      # 라인 위치
        line = [-1,4,8,10,6][n]
        leaf = 'x0xabcdefgh0x0x'
        for i,j in [[1,'b'],[7,-1]]:
            m = sort(m,leaf,i,j)
        for i in range(1,7):
            m = bfs(2,m,leaf,[3,4,5,8,11,10,9,6],'acfhgd',i)
        fix = []
        bfs(1,m,leaf,-1,-1)
    if t is 1:
        n = m.index('x')
        leaf = list('ijklmnop0000')
        leaf.insert(n,'x')
        leaf.remove('0')
        leaf = ''.join(leaf)
        li = {4:[0,8,1], 5:[4,0,8], 6:[7,3,11], 7:[3,11,2]}
        for i in li[n]:
            m = sort(m,leaf,i)
        bfs(1,m,leaf,-1,-1)
    if t is 2:
        global hold
        leaf = ['0'] * 16
        xli = [i for i in range(16) if m[i] is 'x']
        li = list('qrstuvwyz')
        for i in [0,1,2,3,7,6,5,4,8,9,10,11,15,14,13,12]:
            if i in xli:
                leaf[i] = 'x'
            elif li:
                p = li[0]
                leaf[i] = p
                li.remove(p)
        leaf = ''.join(leaf)
        
        hold = {}
        pos = [i for i in [5,6,9,10] if i in xli]
        if pos:
            pos = pos[0]
            # 고정팩 위치 : [첫 번째 정렬 위치 2개, 두 번째 정렬 위치 3개]
            li = {5:[3,7,15,11,14], 6:[0,4,12,8,13],
                  9:[0,1,3,2,7], 10:[3,2,0,1,4]}[pos]
            li = [i for i in li if i not in xli]
            for i in li:
                p = leaf[i]
                if p is '0' and i not in [0,3,12,15]:
                    # 가장 가까운 정렬값이 있는 위치
                    pos0 = bfs(-1,m,leaf,i)[-1]
                    p = leaf[pos0]
                    hold[pos0] = p
                m = sort(m,leaf,i,p)
            li = {5:[1,2,6,10,9,8,4,0], 6:[2,3,7,11,10,9,5,1],
                  9:[5,6,10,14,13,12,8,4,0], 10:[6,7,11,15,14,13,9,5]}[pos]
            li0 = ''.join([leaf[i] for i in li
                           if leaf[i] is not '0' and i not in hold])
            for i in range(1,len(li0)+1):
                m = bfs(2,m,leaf,li,li0,i)
            fix = []
            for i in range(16):
                if leaf[i] not in '0x' and i not in hold:
                    m = bfs(1,m,leaf,i,leaf[i])
            for i in hold:
                m = bfs(1,m,leaf,i,leaf[i])    
        else:
            li = [0,1,4,3,2,7]
            for i in li:
                if leaf[i] not in '0x':
                    m = sort(m,leaf,i)
            bfs(1,m,leaf,-1,-1)
    return res

if __name__ == '__main__':
    
##    Type,root,line = 0,'xcx0aeb0d0hgxfx',2
##    Type,root = 1,'pm00xnok0ijl'
    
##    5  : 'yzrwxtx0qvsu0x0x', 
##    6  : 'r00vzx0xwyqusxtx'
##    9  : 'xwxtuzq0vxs00yrx'
##    10 : 'uxrxz0s0vyxqxw0t'
##    not in center : 'xyr0uwzxt00vxsqx'
    
    Type,root = 2,'x0zr0wxqxtyuvsx0'

    ts = time()    
    res = main(Type,root,-1 if Type else line)    
    te = time() - ts
##    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))

