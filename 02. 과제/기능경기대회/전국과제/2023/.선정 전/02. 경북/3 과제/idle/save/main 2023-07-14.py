from collections import deque
from time import time

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
    for i in range(size) if n > 0 else [pos]:       
        if (n > 0 and m[i] != '0') or i in fix:
            continue
        for j in [j for j in aro(i)
                  if m[j] not in ('0x' if n > 0 else 'x') and j not in fix]:
            if t is 0:
               if (abs(i-j) is 7 and i < 8) or \
                   (j < 8 and i not in [8,15]) or \
                   (i < 8 and j not in [8,15]):
                    continue
            if t is 2 and n:
                pass
                li = [m[k] for k in hli]
                if li != ['0','0'] and j not in hli:
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
    if n in [2,3]:
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
        if n in [2,3]:
            li1 = ''.join([cur[i] for i in li if cur[i] is not '0'])
            if (n is 2 and li0[:n0] in li1) or \
               (n is 3 and li0 in li1 and cur[n0] is leaf[n0]):
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
    if m[e] is not pack:
        res = []
        s = m.index(pack)
        hold = -1
        li = exp(0,m,e)
        b = t is 2 and len(li) is 1
        if b:
            m = bfs(1,m,leaf,e,'0')            
        r = bfs(0,m,s,e)
        if b and all([i not in r for i in hli]):
            fix.append(e)
            hold = e
        if t is 2:
            r = [i for i in r if i not in hli]            
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
                h[li[i]] = i                
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
        if pos:         # 중앙에 고정팩 있을때
            pos = pos[0]        # 중앙 고정팩 위치
            
            sli = {5:[3,7,15,14,11,12,13], 6:[0,4,12,13,8,15,14],
                  9:[0,1,3,2,7,15,11], 10:[3,2,0,1,4,8,12]}[pos]       # 윤곽 정렬 위치
            vt = {5:15,6:12,9:3,10:0}[pos]      # 꼭짓점 위치
            
            # 교환 위치 정하는거 다시짜셈
            # - 홀 안됨
            # - 꼭짓점 안됨
            # - 고정팩 안됨
            pos0 = [i for i in sli
                    if i not in hli and i is not vt and m[i] is not 'x'][0]       # 교환 위치

            # 교환 위치, 고정 팩 : 정렬 x
            # 홀 위치 : 빈칸으로 고정
            for i in sli:
                if m[i] is 'x' or i is pos0:
                    continue
                if i in hli:        # 윤곽에 있는 홀 고정
                    m = bfs(1,m,leaf,i,'0')
                    fix.append(i)
                    continue
                p = leaf[i]
                if p is '0' or i in hold:       # 정렬 위치에 팩이 없음
                    n = bfs(-1,m,leaf,i,list(hold.keys())+[pos0])[-1]         # 가장 가까운 정렬 팩이 존제하는 위치
                    p = leaf[n]      # " 에 있는 팩
                    hold[n] = i      # {원래 정렬 위치:홀딩 위치}
                m = sort(m,leaf,i,p)

            li = {5:[1,2,6,10,9,8,4,0], 6:[2,3,7,11,10,9,5,1],
                  9:[5,6,10,14,13,12,8,4], 10:[6,7,11,15,14,13,9,5]}[pos]
            li0 = [i for i in li if i not in hold]
            li1 = ''.join([leaf[i] for i in li0 if leaf[i] is not '0'])
            
            for i in range(1,len(li1)+1):       # 초밥 정렬
                m = bfs(2,m,leaf,li0,li1,i)
                
            m = bfs(3,m,leaf,li0,li1,pos0)       # 교환 위치 정렬
            fix.append(pos0)

##            printf(leaf,4,4)
##            printf(m,4,4)
            for i in li0:       # 홀드 빼고 정렬
                if leaf[i] not in '0x':
                    m = bfs(1,m,leaf,i,leaf[i])
                    fix.append(i)
            
            for i in hold:
                fix.remove(hold[i])

            fix = []            
            m = bfs(1,m,leaf,-1,-1)
        else:
            pass
        
    return res

if __name__ == '__main__':
    
##    Type,root,leaf= 0,'6x0xx0x870453120','0x0xx0x015286743'
    Type,root,leaf = 1,'xx0xxx867x01x20x543xxxxxx','xx0xxx764xx2x10x358xxxxxx'
##    Type,root,leaf,a = 2,'0034x0x06108052x','0560x0x41203800x',[0, 5]       # 원래거
##    Type,root,leaf,a = 2,'x60032048x01050x','x20050003x18640x',[14, 6]
    
    ts = time()    
    res = main(Type,root,leaf,a if Type is 2 else -1)    
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
