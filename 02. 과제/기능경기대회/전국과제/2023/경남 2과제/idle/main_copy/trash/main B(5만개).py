from collections import deque
from time import time

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    step = [e,s] if li == -1 else li
    pack = 'abc'.index(m[s])+10 if m[s].isalpha() else int(m[s])
    info = ([ing] if t == 0 else [])+[step,pack]
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

def exp(n,m,pos=-1,p:'B 파레트 길찾기' = -1):
    res = []
    if t == 0:
        hli0 = hli[ing]
    if t == 1:
        hli0 = hli[:]
    for i in range(size) if n > 0 else [pos]:
        if (n > 0 and m[i] != '0') or i in fix:
            continue
        if t < 2 and n > 0 and i in hli0:
            continue
        for j in aro(i):
            b = lambda pos: \
                m[pos] not in (['0x','x'][t < 2] if n > 0 else 'x') and pos not in fix
            if not b(j):
                continue
            if t < 2 and n > 0:
                if j in hli0:
                    li = [j]
                    for hp in li:           # hole position
                        li0 = [li[0]] + ([] if hp == li[0] else [hp])        # 'li' init state coped                        
                        for k in aro(hp):
                            if not b(k) or k in li:
                                continue
                            if m[k] == '0':
                                if k in hli0:
                                    li.append(k)
                                continue
                            if t is 1:
                                if (hli0[1] in li0 and m[k] in '789abc') or \
                                   (hli0[2] in li0 and m[k] in '123456'):
                                    continue 
                            res.append(exc(m,i,k,([i]+li0+[k])[::-1]))                        
                if m[j] == '0':
                    continue
            if t == 1 and n < 1 and p != -1:
                if (p in '123456' and j == hli0[2]) or \
                   (p in '789abc' and j == hli0[1]):
                    continue
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def bfs(n,m,*a,p:'B 파레트 길찾기' = -1):
    global res,fix
    if n < 1:       # 길찾기
        s,e = a
    if n == 1:          # 정렬
        leaf,pos,pack = a
    if n == 2:      # 빈칸 정렬
        li, = a
    if n == 3:      # 특정 위치 정렬
        leaf,li = a
    if n == 4:
        li,limit = a
        ct = 0
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        if n == 4:
            if all([cur[i] == '0' for i in li]):
                return False
            if ct > limit or not que:
                return True
            ct += 1
        if n == -1 and not que:
            if e == -1:
                return list(mkd.keys())
            return -1
        cur = que.popleft()
        if n < 1 and cur == e:
            break
        if n == 1:
            if (pos == -1 and cur == leaf) or \
               (pos != -1 and cur[pos] == pack):
                break
        if n == 2 and all([cur[i] == '0' for i in li]):
            break
        if n == 3:
            if all([cur[i] == leaf[i] for i in li]):
                break
        for i,j in exp(n,cur if n > 0 else m,cur,
                       p if t == 1 and p != -1 else -1):
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
        
def sort(m,leaf,e,p = -1):
    global fix,res
    pack = leaf[e] if p is -1 else p
    if t is 1:
        
##        print('팩 -> {}, 위치 -> {}'.format(pack,e))        
        ct = 0
        while 1:
            s = m.index(pack)       # 정렬할 팩 위치
            r = bfs(0,m,s,e,p = pack)       # 정렬 위치까지 경로
            if len([i for i in r if i not in hli]) > 4:      # 빈칸이 5이상 필요한 경우
                pos1 = r[ct]
                m = sort(m,leaf,pos1,pack)
                fix.remove(pos1)
                ct += 1
                continue
            fix.append(s)       # 출발지 고정
            road = []         # 뚫을 경로
            for pos in r[::-1]:               
                pack1 = m[pos]
                if pack1 == '0':        # 원래 치워져 있지롱
                    road.append(pos)
                    continue
                
                b = False
                if bfs(4,m,[pos]+road,5000):
                    b = True
                        
                if b:
##                    print('막혔음 fix ->',fix)
##                    print('road+[pos] ->',road+[pos])
##                    print('-> {} 고정 해제'.format(s))
##                    printf(m,4,5)
                    fix.remove(s)

                road.append(pos)
                
                m = bfs(2,m,road)
##                print(road,'DDOING')
##                printf(m,4,5)
                
            if s in fix:        # 출발위치를 고정을 안풀고 road를 다 비웠을때 break
                break            
        fix.remove(s)       # 출발지 고정 해제
        m,step = exc(m,e,s,[s]+r)
        res.append(step)
##        print('='*50)
        
    else:
        s = [i for i in range(size) if i not in fix and m[i] == pack][0]        # A가 팩이 여러개라 이렇게 함
        r = bfs(0,m,s,e)
        if t < 2:
            r = [i for i in r if i not in (hli if t else hli[ing])]         # B 에서 안쓸거면 줄이셈
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
    cache = {}      # cache reset
    if t in [0,1]:
        global hli
    if t == 1:
        leaf,hli = a     
        hold = []           # 홀딩 중인 팩
        unhold = []         # 정렬 위치 경로
        def getli(li,n):
            li1 = []
            li2 = [i+n in hli[1:] for i in li]
            if (li2[2] and li2[3]) or \
               (li2.count(1) == 1 and li2[2]):
                li1 = li[::-1]
            elif not (li2.count(1) == 1 and li2[1]):
                for i in li:
                    if i+n in hli[1:]:
                        li1.append(i)
            li1 += [i for i in li if i not in li1]
            return li1        
        li = []         # 정렬 순서
        if all([i in [3,4,8,9,13,14,18,19] for i in hli[1:]]):
            for i in [[4,9,14,19],[3,8,13,18],[2,7,12,17]]:
                li += getli(i,-1)
        else:
            for i in [[0,5,10,15],[1,6,11,16],[2,7,12,17]]:
                li += getli(i,1)
        
        for pos in li:            
            if pos in hli:      # 정렬 위치가 홀
                continue            
            # 정렬할 팩
            if leaf[pos] is '0' or leaf[pos] in hold:         
                li1 = []         # [pack,road]
                for i in range(size):
                    if i not in fix and leaf[i] not in hold+['0']:
                        pack = leaf[i]
                        # 각 팩에서 길찾기를 할때 홀딩중이지 않은 팩을 넘을 수 없음
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
            if m[pos] == pack:      # 이미 정렬됨 fix, continue
                fix.append(pos)
                continue
##            print(pos,pack)
##            print(fix)
##            printf(m,4,5)
            m = sort(m,leaf,pos,pack)            
        li = [m[i] for i in range(size) if i not in fix and m[i] != '0']        # 고정 안된 팩
        li = [leaf.index(i) for i in li]        # " 위치
        m = bfs(3,m,leaf,li)        
        for r in unhold[::-1]:
            m,step = exc(m,r[-1],r[0],r)
            if any([m[i] != '0' for i in step[0]][:-1]):
                print('다시 가져오는 길이 막힘\nunhold ->',unhold[::-1],'-',r)
                exit()
            res.append(step)
            
    if t == 2:
        pass
    
    return res

if __name__ == '__main__':
    
##    t,m1,m2,a = 0,'051002426053060','510642030314000',[[0, 9, 14], [2, 6, 12]]

    # loop
##    t,m1,m2,a = 1,'0507a2804b00c0306019','c0b90a13040020670850',[11, 10, 13]
##    t,m1,m2,a = 1,'c007ba40183020509006','a0890b006370c0105402',[11, 1, 13]
##    t,m1,m2,a = 1,'21965c4a00083070b000','0060c398010750ba0042',[10, 17, 8]
    
    # short limit
##    t,m1,m2,a = 1,'73c410009600280a0b05','182cb0079000a0640503',[11, 10, 6]         # limit 2000 -> 3000
##    t,m1,m2,a = 1,'0000c24073809a6100b5','b800136405c02790000a',[17, 2, 16]         # limit 3000 -> 3500
##    t,m1,m2,a = 1,'007080291ba360c00054','400096a5b8c237001000',[1, 3, 17]          # limit 3500 -> 4000
##    t,m1,m2,a = 1,'0ab971c2800030500640','00310098c204b0a07560',[15, 13, 19]        # limit 4000 -> 5000
    t,m1,m2,a = 1,'67c900010ab400305802','3a0009460c07002105b8',[12, 8, 13]
        
    ts = time() 
    res = main(t,m1,m2,a)
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,6),int((te*250)//60),int((te*250)%60)))
