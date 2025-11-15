from collections import deque
from time import time
from printer import printf

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    step = [e,s] if li is -1 else li
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

def exp(n,m,pos=-1):
    res = []
    for i in range(size) if n > 0 else [pos]:       
        if (n > 0 and m[i] is not '0') or i in fix:
            continue
        if t is 2 and n > 0 and i in hli:        # 홀 위에는 팩을 둘 수 없음
            continue        
        for j in aro(i):
            b = lambda pos: m[pos] not in (['0x','x'][t is 2] if n > 0 else 'x') and pos not in fix
            if not b(j):
                continue            
            if t is 0:
               if (abs(i-j) is 7 and i < 8) or \
                   (j < 8 and i not in [8,15]) or \
                   (i < 8 and j not in [8,15]):
                    continue
            if t is 2 and n > 0:                
                if j in hli:
                    li = [j]
                    for hp in li:       # hole position
                        li0 = li[:]         # 'li' init state coped
                        for k in aro(hp):
                            if b(k) and k not in li:
                                if m[k] is '0':
                                    if k in hli:
                                        li.append(k)
                                    continue
                                res.append(exc(m,i,k,([i]+li0+[k])[::-1]))
                if m[j] is '0':         # 0 끼리 교체 컨티뉴(홀 처리 이후)
                    continue
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res
  
def bfs(n,m,*a):
    global res
    if n is -1:
        leaf,s,li = a 
    if n is 0:
        s,e = a
    if n is 1:
        leaf,pos,pack = a
    if n > 1:
        leaf,li,li0,n0 = a
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n is -1 and \
           leaf[cur] is not '0' and cur not in li:
            break
        if n is 0 and cur == e:
            break
        if n is 1:
            if (pos is -1 and cur == leaf) or \
               (pos is not -1 and cur[pos] == pack):
                break
        if n > 1:       # 회전 초밥 정렬
            li1 = ''.join([cur[i] for i in li if cur[i] is not '0'])
            if n is 2 and li0[:n0] in li1:
                break
            if n is 3 and li0 in li1 and cur[n0] is leaf[n0]:
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
    if n > 0 :
        res += path[::-1][1:]
        return mkd[-2]
    return path[::-1][1:]

def sort(m,leaf,e,p=-1):
    pack = leaf[e] if p is -1 else p
    res = []
    s = m.index(pack)    
    r = bfs(0,m,s,e)
    if t is 2:
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
    cache = {}      # cache reset
    if t is 0:
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
    if t is 1:
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
        vt = {5:15,6:12,9:3,10:0}       # 꼭짓점 위치
        if pos:
            pos = pos[0]        # 중앙 고정팩 위치                    
            li = {5:[3,12,7,13,15,14,11], 6:[0,15,4,14,12,13,8],
                  9:[0,15,1,11,3,2,7], 10:[3,12,2,8,0,1,4]}[pos]       # 윤곽 정렬 위치
            li0 = {5:[1,2,6,10,9,8,4,0], 6:[2,3,7,11,10,9,5,1],
                  9:[5,6,10,14,13,12,8,4], 10:[6,7,11,15,14,13,9,5]}[pos]         # 회전 초밥 위치
            b = lambda n:n not in hli and n is not vt[pos] and m[n] is not 'x'       # 홀 x, 꼭짓점x, 고정 팩x
            pos0 = [i for i in li if leaf[i] is '0' and b(i)]
            pos0 = pos0[0] if pos0 else [i for i in li if b(i)][0]            
            for i in li:
                if i not in hli and i is not pos0 and m[i] is not 'x':
                    if leaf[i] is '0' or i in hold:
                        pos1 = bfs(-1,m,leaf,i,hold)[-1]
                        m = sort(m,leaf,i,leaf[pos1])
                        hold[pos1] = i
                    else:
                        m = sort(m,leaf,i)
            li1 = ''.join([leaf[i] for i in li0 if i not in hold and leaf[i] is not '0'])
            for i in range(1,len(li1)+1):
                m = bfs(2,m,leaf,li0,li1,i)            
            if pos0 in hold:
                fix.remove(hold[pos0])
                del hold[pos0]
            m = bfs(3,m,leaf,li0,li1,pos0)
            fix.append(pos0)
            for i in li0:
                if i not in hold and leaf[i] is not '0':
                    m = bfs(3,m,leaf,li0,li1,i)
                    fix.append(i)                    
            for i in hold:
                fix.remove(hold[i])
            if m[pos0] is '0':
                fix.remove(pos0)
            m = bfs(1,m,leaf,-1,-1)
        else:
            ct = 0
            li = [0,3,12,15,1,2,13,14]
            for i in li:
                if leaf[i] not in '0x':
                    m = sort(m,leaf,i)
                if leaf[i] is '0':
                    if ct > 2:
                        m = bfs(1,m,leaf,i,'0')
                        fix.append(i)
                    ct += 1            
                
            print('fix ->',fix)
            print('hold ->',hold)
            print('count ->',ct)
            print('H pos')
            printf(''.join(['H' if i in hli else ' ' for i in range(16)]),4,4)
            print('leaf')
            printf(leaf,4,4)
            print('root')
            printf(m,4,4)
        
    return res

if __name__ == '__main__':
    
##    Type,root,leaf= 0,'6x0xx0x870453120','0x0xx0x015286743'
##    Type,root,leaf = 1,'xx0xxx867x01x20x543xxxxxx','xx0xxx764xx2x10x358xxxxxx'
    Type,root,leaf,a = 2,'0x0x065031428x70','0x0x073852610x40',[15, 0]
    
    ts = time()    
    res = main(Type,root,leaf,a if Type is 2 else -1)    
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
