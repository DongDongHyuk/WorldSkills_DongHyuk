from collections import deque
from time import time
from printer import printf

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    step = [e,s] if li is -1 else li
    p = int(m[s])
    return [''.join(m),[step,p]]
    
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

def exp(n,m,pos):
    res = []
    for i in range(size) if n > 0 else [pos]:       
        if (n > 0 and m[i] is not '0') or i in fix:
            continue
        for j in [j for j in aro(i)
                  if m[j] not in ('0x' if n > 0 else 'x') and j not in fix]:
            if t is 0:
               if (abs(i-j) is 7 and i < 8) or \
                   (j < 8 and i not in [8,15]) or \
                   (i < 8 and j not in [8,15]):
                    continue
            if t is 2 and n is -1 and m[i] is not '0':
                continue
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def exp0(*m):        # 정렬 - 팩을 들고 갈 수 있는 모든곳
    m = m[1 if len(m) is 3 else 0]
    res = []
    for i in range(size):
        if m[i] is '0' and i not in fix:
            mkd,step = bfs(-1,m,i)
            for j in mkd:
                if i is not j and i not in hli and j not in fix and \
                   m[j] not in '0x':
                    r = path(mkd,step,j)[::-1]+[i]
                    res.append(exc(m,i,j,r))
    return res

def bfs(n,m,*a):
    global res
    if n is -1:
        s, = a
    if n is 0:
        s,e = a
    if n is 1:
        leaf,pos,pack = a
    if n is 2:
        leaf,li,li0,n0 = a
    expand = exp0 if n > 0 and t is 2 else exp      # C 파레트 정렬일때 exp0
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        if n is -1 and not que:
            return mkd,step
        cur = que.popleft()
        if n is 0 and cur == e:
            break
        if n is 1:
            if (pos is -1 and cur == leaf) or \
               (pos is not -1 and cur[pos] == pack):
                break
        if n is 2:
            li1 = ''.join([cur[i] for i in li if cur[i] is not '0'])
            if li0[:n0] in li1:
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
    cur = mkd[-2] if cur is -1 else cur
    path = [step[cur]]
    while mkd[cur] != -1:
        cur = mkd[cur]
        path.append(step[cur])
    return path[::-1][1:]

def sort(m,leaf,e,p=-1):
    pack = leaf[e] if p is -1 else p
    res = []
    s = m.index(pack)
    r = bfs(0,m,s,e)
    for i in r:
        if t is 2 and i in hli:
            continue
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
    if t == 2:        
        global hli
        leaf,hli = a

        hold = {}       # 정렬 위치에 팩이 없을때 가까운 팩을 가져와서 홀딩
        xli = [i for i in range(16) if m[i] is 'x']         # 고정팩 위치
        pos = [i for i in [5,6,9,10] if i in xli]           # 중앙에 있는 고정팩
        if pos:
            pos = pos[0]        # 중앙 고정팩 위치                    
            li = {5:[3,7,12,13,15,14,11], 6:[0,4,15,14,12,13,8],
                  9:[0,1,15,11,3,2,7], 10:[3,2,12,8,0,1,4]}[pos]       # 윤곽 정렬 위치
            li0 = {5:[1,2,6,10,9,8,4,0], 6:[2,3,7,11,10,9,5,1],
                  9:[5,6,10,14,13,12,8,4,0], 10:[6,7,11,15,14,13,9,5]}[pos]         # 회전 초밥 위치
            vt = {5:15,6:12,9:3,10:0}[pos]      # 꼭짓점 위치

            # 팩 교환 위치부터 정해보자고
            b = lambda n:n not in hli and n is not vt and m[n] is not 'x'       # 홀 x, 꼭짓점x, 고정 팩x
            pos0 = [i for i in li if leaf[i] is '0' and b(i)]
            pos0 = pos0[0] if pos0 else [i for i in li if b(i)][0]
            
            for i in li:
                if m[i] is not 'x':
                    # *** 홀, 교환 위치 포함 ***
                    if leaf[i] is '0':
                        if i is vt:
                            m = bfs(1,m,leaf,i,'0')
                            fix.append(i)
                    else:
                        m = sort(m,leaf,i)
##                        m = bfs(1,m,leaf,i,leaf[i])
##                        fix.append(i)

##            print('pos0 ->',pos0)
##            print('H pos')
##            printf(''.join(['H' if i in hli else ' ' for i in range(16)]),4,4)
##            print('root')
##            printf(m,4,4)
##            print('leaf')
##            printf(leaf,4,4)
##                        
        else:
            pass
        
    return res

if __name__ == '__main__':
    
##    Type,root,leaf= 0,'6x0xx0x870453120','0x0xx0x015286743'
##    Type,root,leaf = 1,'xx0xxx867x01x20x543xxxxxx','xx0xxx764xx2x10x358xxxxxx'
    Type,root,leaf,a = 2,'60x34500x7x82001','00x40512x3x67008',[13, 14]
    
    
    ts = time()    
    res = main(Type,root,leaf,a if Type is 2 else -1)    
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
