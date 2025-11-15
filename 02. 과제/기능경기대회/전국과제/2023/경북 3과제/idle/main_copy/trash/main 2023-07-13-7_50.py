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
        if n is 0 and cur == e:
            break
        # (t is not 2 or [cur[i] for i in hli] == ['0','0']) # 홀 위에 팩없을 때만 종
        if n is 1:
            if cur == leaf or \
               (pos != -1 and cur[pos] == pack):
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
    if n > 0 :
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
        r = [i for i in r if i not in hli]
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
    if t == 2:
        global hli,hold
        leaf,hli = a

        print('hole positions')
        printf(['H' if i in hli else '0' for i in range(16)],4,4)
        print('root')
        printf(m,4,4)
        print('leaf')
        printf(leaf,4,4)

        hold = {}       # 정렬 위치에 팩이 없을때 가까운 팩을 가져와서 홀딩
        xli = [i for i in range(16) if m[i] is 'x']         # 고정팩 위치
        pos = [i for i in [5,6,9,10] if i in xli]           # 중앙에 있는 고정팩
        if pos:         # 중앙에 고정팩 있을때
            pos = pos[0] 
            sli = {5:[3,7,15,14,11,12,13], 6:[0,4,12,13,8,15,14],
                  9:[0,1,3,2,7,15,11], 10:[3,2,0,1,4,8,12]}[pos]       # 정렬 위치 
            li = [i for i in sli if i not in xli+hli]        # 정렬 위치에서 홀이랑 고정팩은 제외
            pos0 = [i for i in li if leaf[i] is '0' and i is not sli[2]]       # 회전초밥에서 팩 교환할 공간
            pos0 = pos0[0] if pos0 else [i for i in li if i is not sli[2]][0]       # pos0 없으면 정렬값 있는곳
            li.remove(pos0)         # pos0은 정렬값에서 제외
            print('교환 위치 ->',pos0)
            print('정렬 리스트 ->',li,'\n')
                
            for i in li: 
                p = leaf[i]
                if p is '0' or i in hold:       # 정렬 위치에 팩이 없거나 홀딩
                    n = bfs(-1,m,leaf,i)[-1]         # 가장 가까운 정렬 팩이 존제하는 위치
                    p = leaf[n]      # " 에 있는 팩
                    hold[n] = p      # hold에 저장
                m = sort(m,leaf,i,p)

            print('첫 번째 정렬 상태')
            printf(m,4,4)
                    
            li = {5:[1,2,6,10,9,8,4,0], 6:[2,3,7,11,10,9,5,1],
                  9:[5,6,10,14,13,12,8,4], 10:[6,7,11,15,14,13,9,5]}[pos]
            li0 = ''.join([leaf[i] for i in li
                           if leaf[i] is not '0' and i not in hold])
            print('초밥 ->',li0) 
            
            for i in range(1,len(li0)+1):
                m = bfs(2,m,leaf,li,li0,i)
            print('두 번째 정렬 상태')
            printf(m,4,4)

            print(fix,hold)

            print(pos0,'에',leaf[pos0])
            if leaf[pos0] is not '0':       # 교환 위치에 정렬 값이 있을때
                if pos0 in hold:
                    fix.remove(m.index(hold[pos0]))
                    hold.pop(pos0)
                m = sort(m,leaf,pos0)
                print('교환 위치 정렬 상태')
                printf(m,4,4)
            
            for i in hold:
                fix.remove(m.index(hold[i]))

            for i in sli:
                m = bfs(1,m,leaf,i,leaf[i])
            print('최종 정렬 상태')
            printf(m,4,4)
        else:
            pass
        
    return res

if __name__ == '__main__':
    
##    Type,root,leaf= 0,'6x0xx0x870453120','0x0xx0x015286743'
##    Type,root,leaf = 1,'xx0xxx867x01x20x543xxxxxx','xx0xxx764xx2x10x358xxxxxx'
    Type,root,leaf,a = 2,'x0x002853x046100','x0x046580x312000',[1, 15]

    ts = time()    
    res = main(Type,root,leaf,a if Type is 2 else -1)    
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
