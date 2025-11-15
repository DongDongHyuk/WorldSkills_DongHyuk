from collections import deque
from time import time
from printer import printf

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
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 2:
        li, = a
    if n == 3:
        leaf,li = a
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
        
        '''
        1. 현재 위치에서 도착위치 까지 길찾기
        2. 팩이 있는 위치를 고정하고, 도착지에서 부터 길을 뚫음
        3. 만약 팩이 있는 위치를 고정해서 뚫어야할 위치에 있는 팩을 치울 공간이 없으면
        4. 출발위치에 고정한거를 고정 풀고 ㄱㄱ
        '''
        
        print('============================')
        print('팩 -> {}, 위치 -> {}'.format(pack,e))
        ct = 0      # PRINT
        while 1:
            ct += 1      # PRINT
            print('{}트'.format(ct))
            s = m.index(pack)       # 정렬할 팩 위치
            r = bfs(0,m,s,e,p = pack)       # 정렬 위치까지 경로
            
            if len([i for i in r if i not in hli]) > 4:      # 빈칸이 5이상 필요한 경우
                pos1 = r[3]
                print('멀어서 도착지에 가깝게 이동 {} -> {}'.format(s,pos1))
                m = sort(m,leaf,pos1,pack)
                fix.remove(pos1)

                ct = 0      # PRINT
                continue
                
            fix.append(s)       # 출발지 고정            
            road = []         # 뚫을 경로
            st = []         # 뚫었던 길중 막힌 곳
            
            for i in r[::-1]:
                if i in hli:
                    continue
                li = [j for j,k in exp(0,m,i,m[i])]         # 스텝 제외
                li = [j for j in li if j not in st]         # 뚫었던 길중 막힌 곳 제외
                for j in li:
                    if j in hli:
                        li1 = [k for k,l in exp(0,m,j) if k != i]       # 홀이 있는데 홀을 타고 갈곳이 없음
                        if not li1:
                            li.remove(j)
                b = m[i] != '0' and not li        # i 에 있는 팩을 치울 공간이 없음
                if b:
                    print('막혔음 fix ->',fix)
                    print('뚫었던 길중 막힌곳 ->',st)
                    print('-> {} 고정 해제'.format(s))
                    printf(m,4,5)
                    fix.remove(s)
                road.append(i)
                m = bfs(2,m,road)
                print(road,'DDOING')
                # 현재 뚫은 위치가 막힌 곳있가
                if len(li) == 1 and li[0] in r:
                    st.append(i)
                printf(m,4,5)
            if not b:
                break
        fix.remove(s)       # 출발지 고정 해제
        m,step = exc(m,e,s,[s]+r)
        res.append(step)
        print('============================\n')
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
        def getli(li,n):
            li1 = []
            li2 = [i+n in hli[1:] for i in li[2:]]
            if all(li2) and len(li2) == 2:
                li1 = li[::-1]
            else:
                for i in li:
                    if i+n in hli[1:]:
                        li1.append(i)
            li1 += [i for i in li if i not in li1]
            return li1        
        hold = []           # 홀딩 중인 팩
        unhold = []         # 정렬 위치 경로
        li = []         # 정렬 순서
        li += [i for i in getli([0,5,10,15],1)]
        li += [i for i in getli([4,9,14,19],-1)]
        li += [i for i in getli([1,2,3],5)]
        for pos in li:
            
            if pos in hli:      # 정렬 위치가 홀
                continue
            
            if len([i for i in fix if m[i] != '0']) == 12:
                break

            # 정렬할 팩
            if leaf[pos] is '0' or leaf[pos] in hold:
                
                # 공사중                
                li1 = []         # [pack,road]
                for i in range(size):
                    if i not in fix and leaf[i] not in hold+['0']:
                        pack = leaf[i]
                        r = [pos]+bfs(0,leaf,pos,i,p = pack)

                        li2 = [leaf.index(j) for j in '123456789abc'
                               if m.index(j) not in fix and j != pack]
                        if not any([j in li2 for j in r]):                        
                            li1.append([pack,r])
                        
                pack,r = min(li1,key = lambda n: len(n[1]))
                
                hold.append(pack)
                unhold.append(r)
            else:
                pack = leaf[pos]
                
            if m[pos] == pack:      # 이미 정렬됨 fix, continue
                fix.append(pos)
                continue

            m = sort(m,leaf,pos,pack)
            
        li = [m[i] for i in range(size) if i not in fix and m[i] != '0']        # 고정 안된 팩
        li = [leaf.index(i) for i in li]        # " 위치
        m = bfs(3,m,leaf,li)

##        print(unhold[::-1])
##        printf(m,4,5)
##        printf(leaf,4,5)        
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

##    t,m1,m2,a = 1,'605a0709038400c0b201','60c50903a0020871040b',[4, 6, 12]      # hmi 예시 배치
##    t,m1,m2,a = 1,'090004200b78a001356c','0b3501006a9c08720004',[0, 4, 7]
##    t,m1,m2,a = 1,'359b01040000c6802a07','5103460b97080c2a0000',[18, 10, 6]

    # Failed List    
##    t,m1,m2,a = 1,'68007030005004cb92a1','20b90700a60003814c50',[11, 7, 12]         # 가져오는길 막힘
    t,m1,m2,a = 1,'0000c250630148ab9070','530240a00700018bc096',[2, 17, 7]

##    printf(m1,4,5)

        
    ts = time() 
    res = main(t,m1,m2,a)
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,6),int((te*250)//60),int((te*250)%60)))
