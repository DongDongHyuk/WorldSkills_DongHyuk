from collections import deque
from time import time
from printer import printf
from rdm import rdm

def exc(m,s,e,ct=-1,dire=-1,rtt=0):
    m = list(m)
    if not rtt:
        m[s],m[e] = m[e],m[s]
    pack = -1 if rtt else ('abc'.index(m[s])+10 if m[s].isalpha() else int(m[s]))
    info = [[e,s],pack]
    info = info + [rtt] if t == 0 else info
    if t == 0:
        ct += (1 if dire in [1,3,5,7] else abs(rtt)) if rtt else -1
        m = (''.join(m), ct, dire)        
    else:
        m = ''.join(m)    
    return [m,info]
    
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
    if t == 0:
        m,ct,dire = m       # 맵, 카운트, 인덱스 방향        
        if n > 0 and not ct:        # 카운트가 없을때 인덱스 회전
            
##            li = [1,3,5,7,0,2,4,6]
##            for i in li[(4 if dire in li[:4] else 0):]:
##                if i == dire:
##                    continue
##                res.append(exc(m, -1, -1, ct, i, i - dire))

            li = [1,-1,2,-2,3,-3,4]
            li1 = [1,3,5,7]
            for i in li:
                ndire = abs(dire + i) % 8
                if dire in li1 and ndire in li1:
                    continue
                res.append(exc(m, -1, -1, ct, ndire, i))                
            return res
        
    for i in range(size) if n > 0 else [pos]:       
        if (n > 0 and m[i] != '0') or i in fix:
            continue
        for j in [j for j in aro(i) if m[j] not in ['x','0x'][n > 0] and j not in fix]:
            if t == 0 and n > 0:      # A 파레트 방향 조건
                mdire = i - j       # 현재 방향
                idire = {-4 : [0, 1, 7], 1 : [1, 2, 3], 4 : [3, 4, 5], -1 : [5, 6, 7]}[mdire]       # 방향 : 인덱스 방향
                if dire not in idire:
                    continue
            res.append((exc(m,i,j,ct,dire) if t == 0 else exc(m,i,j)) if n > 0 else [j,j])
    return res

def bfs(n,m,*a):
    global res
    if n == -1:
        leaf,s = a
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        if n == 2 and not que:
            return 0
        cur = que.popleft()
        if n == -1 and leaf[cur] != '0'and cur not in hold:
            break
        if n == 0 and cur == e:
            break
        if n == 1:
            cur1 = cur[0] if t == 0 else cur
            if ((pos == -1 and cur1 == leaf) or (pos != -1 and cur1[pos] == pack)) and \
               (t != 0 or (t == 0 and bfs(2,cur))):
                break
        if n == 2 and not cur[1]:      
            return 1        
        for i,j in exp(n,cur if n > 0 else m,cur):
            if i not in mkd:                
                que.append(i)
                mkd[i],step[i] = cur,j
    mkd[-2] = cur

    # temp
    if n > 0:
        path = [(cur,step[cur])] 
    else:
        path = [step[cur]]
    # >>>
    # path = [step[cur]]

    while mkd[cur] != -1:
        cur = mkd[cur]

        # temp
        if n > 0:
            path.append((cur,step[cur]))
        else:
            path.append(step[cur])
        # >>>
        # path.append(step[cur]) 

    if n > 0:
        res += path[::-1][1:]
        return mkd[-2]
    return path[::-1][1:]
    
def sort(m,leaf,e,p=-1):        # A 파레트만 사용
    pack = leaf[e] if p == -1 else p
    if pack != '0':
        s = m[0].index(pack)
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
    sy,sx = [[4,4],[0,0],[0,0]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}      # cache rese5t
    if t == 0:
        global hold
        leaf,dire = a
        ct = 1
        m = (m, ct, dire)      # m, count, indexDire(0 ~ 7)

        # printingRoot
        print(' R O O T \n count : {}, indexDire : {}'.format(ct,dire))
        printf(m[0],4,4)

        # exp test
##        for i,j in exp(1,m):
##            a,b,c = i
##            print(' count : {}, indexDire : {}'.format(b, c))
##            printf(a,4,4)

        
        fp = leaf.index('x')
        # if fp in [5,6,9,10]:
        #     li = {5 : [12,15,13,14], 6 : [], 9 : [], 10 : []}[fp]
        # else:
        #     pass
        
        li = [15,12,13,14]        # temp

        hold = {}
        for i in li:
            pack = leaf[i]
            if pack == '0':         # 정렬 위치에 팩이 없을때 가까운 팩 찾기
                pos = bfs(-1,m,leaf,i)[-1]
                pack = leaf[pos]
                hold[pos] = pack

##            print('sorting,,, pos -> {}, pack -> {}'.format(i,pack))
            m = sort(m,leaf,i,pack)
##            printf(m[0],4,4)

        
    if t == 1:
        pass
    if t == 2:
        pass
    return res

if __name__ == '__main__':

    t = 0
    # r,l,dire = rdm(0)
    r,l,dire = '020bcxa765813904','6b102x50843907ac',3
    # r,l,dire = '12345x6789abc000','12345x069007c8ab',3        # 예시 배치
        
    ts = time()    
    res = main(t,r,l,dire)
    te = time() - ts
    
    # PrintingResult
    for cur,info in res:
        m,ct,dire = cur
        se,pack,rtt = info
        isRtt = info[0] == [-1]*2
        if isRtt:
            print('indexRotate,,, rtt : {}, ct : {}, indexDire : {}'.format(rtt,ct,dire),'\n')
        if not isRtt:
            s,e = se
            print(' pack : {} | {} to {}'.format(pack,s,e))
            printf(m,4,4)

    reslen = len([i for i in res if i[1][0] != [-1,-1]] if t == 0 else res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(reslen,round(te,3),int((te*250)//60),int((te*250)%60)))
