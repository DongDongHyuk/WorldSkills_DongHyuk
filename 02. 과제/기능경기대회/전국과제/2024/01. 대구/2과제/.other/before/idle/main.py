from collections import deque
from time import time
from printer import printf

def exc(m,s,e):
    if t == 0:
        m,gli,g = m
        m,gli = map(list,[m,gli])           # tuple -> list
        n = gli.index('0' if g else e)
        gli[n] = m[s] if g else '0'         # 그립 리스트 수정
        m[s] = '0' if g else e              # 맵 수정
        info = [s,int(m[s]),g,n]            # 위치, 팩, 그리퍼상태, 그리퍼종류
        ct = gli.count('0')
        g = 0 if (ct == 0 and g) else 1 if (ct == 2 and not g) else g       # 다음 그리퍼 상태
        m = (''.join(m),''.join(gli),g)
    else:
        istp = type(m) == tuple
        if t == 2 and istp:
            m,ct = m
            ct -= 1
        m = list(m)
        m[s],m[e] = m[e],m[s]

        info = [[e,s],int(m[s])]        # makikng info        
        if t == 2:
            if m[s] != '1':
                info.append(int(m[e]))
            if istp:
                info.append(ct)

        m = ''.join(m)
        if t == 2 and istp:
            m = (m,ct)
    return [m,info]

def aro(pos):
    res = []
    if t == 1:
        dx = [-4,-3,-2,-1,1,2,3,4]
        res += [i for i in [pos + i for i in dx] if -1 < i < 9]
    if t == 3:
        res += [[1],[0,2,3],[1,4],[1,4],[2,3,5,6],[4,7],[4,7],[5,6,8],[7]][pos]
    return res

def exp(n,m,pos=-1):
    res = []
    if t == 0:
        m,gli,g = m
    if t == 2:
        m,ct = m
        y,x = divmod(m.index('1'),3)
        li1 = [i for i in range(9) if m[i] == '0']
        li2 = [i for i in range(9) if m[i] not in '01' and i not in fix and (i // 3 == y or i % 3 == x)]
        if len(li2) == 2:       # 라인 변경
            m1 = m[:]
            step = []
            pack = []
            for i,j in zip(li1,li2):
                m1,info = exc(m1,i,j)
                step.append(info[0]), pack.append(info[1])
            info = step + pack
            line = sorted(li2 + [m1.index('1')])
            line = [i for i in line if m[i] != '1']
            res.append([(m1,3),info + [line] + [3]])
        if ct == 0:         # 카운트가 0일때 무조건 라인 변경
           return res 
    for i in range(9) if n > 0 else [pos]:
        if i in fix:        # 고정위치
            continue
        if t == 0:
            b1 = not g and (m[i] != '0' or (i > 2 and m[i - 3] in '01'))        # 놓기(기본 규칙, 3차원 규칙, 원형팩 규칙)
            b2 = g and (m[i] == '0' or (i < 6 and m[i + 3] != '0'))             # 잡기(기본 규칙, 3차원 규칙)  
            if b1 or b2:
                continue
            if g:
                res.append(exc((m,gli,g), i, -1))
            else:
                for pack in gli:
                    res.append(exc((m,gli,g), i, pack))
            continue            
        if n > 0 and m[i] != '0' and t != 2:
            continue        
        li = [None, aro(i), range(9), aro(i)][t]
        for j in [j for j in li if (n < 1 or m[j] != '0') and j not in fix]:
            if t == 1:
                pack = m[j]
                b1 = pack != '1' and i - j in [-4,4]        # 사각팩 이동거리 제한
                b2 = False
                if pack == '1':                             # 원형팩 이동규칙
                    a,b = sorted([i,j])
                    li = m[a + 1 : b]
                    b2 = not li or any([k not in '246' for k in li])
                if b1 or b2:
                    continue
            if t == 2:
                li1 = [m[i],m[j]]
                if i == j or ('1' in li1 and '0' not in li1) or ('0' in li1 and '1' not in li1):
                    continue
            res.append(exc((m,ct),i,j) if t == 2 else exc(m,i,j) if n > 0 else [j,j])
    return res

def bfs(n,m,*a):
    global res
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 2:
        li, = a
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n == 0 and cur == e:
            break
        if n == 1:
            cur1 = cur[0] if t in [0,2] else cur
            if (pos == -1 and cur1 == leaf) or \
               (pos != -1 and cur1[pos] == pack):
                break
        if n == 2 and all([i in '246' for i in [cur[i] for i in li]]):
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

def main(g_t,m,*a):    
    global t,fix,res
    t = g_t
    fix = []
    res = []
    if t == 0:
        leaf, = a
        m = (m,('0','0'),1)
        for i in range(3):
            if leaf[i] not in '01':
                m = bfs(1,m,leaf,i,leaf[i])
                fix.append(i)
        bfs(1,m,leaf,-1,-1)
    if t == 1:
        leaf, = a
        cur = m.index('1')
        end = leaf.index('1')
        while cur != end:            
            fix.append(cur)
            n = abs(cur - end)
            e = (cur + 4 if cur < end else cur - 4) if n > 4 else end
            road = list(range(cur,e,1 if cur < e else -1))[1:]
            if n != 1:
                m = bfs(1,m,leaf,e,'0')
                fix.append(e)
                m = bfs(2,m,road)
            fix = []            
            m = bfs(1,m,leaf,e,'1')
            cur = e
        fix.append(end)
        for i in [0,1,2] if m.index('1') > 4 else [8,7,6]:
            if leaf[i] != '0':
                m = bfs(1,m,leaf,i,leaf[i])
                fix.append(i)
        bfs(1,m,leaf,-1,-1)
    if t == 2:
        leaf,ct = a
        m = (m,ct)
        pos = leaf.index('1')
        y,x = divmod(pos, 3)
        li = [i for i in range(9) if i // 3 == y or i % 3 == x]
        m = bfs(1,m,leaf,pos,'1')       # 1부터 정렬
        fix.append(pos)
        for i in range(9):
            if i not in li:
                m = bfs(1,m,leaf,i,leaf[i])
                fix.append(i)
        bfs(1,m,leaf,-1,-1)
    if t == 3:
        leaf = '123456700'
        for e in range(7):
            pack = leaf[e]
            s = m.index(pack)
            road = bfs(0,m,s,e)
            for j in road:
                m = bfs(1,m,leaf,j,pack)
            fix.append(e)
    return res

# [ A ]
# 초기 배치 랜덤
# 정렬 배치 랜덤
# 원형팩위에 배치 불가

#     대 중 소
# 원형 1, 0, 0 (1개)
# 사각 0, 3, 3 (3개)

# 4칸 이상 쌓을 수 없음
# 팩을 이동시킬때 무조건 2개씩 잡고 2개씩 놓아야함

# 원형
# - 항상 제일 위에 있어야함(원형팩 위에 팩을 적재 할 수 없음)


# [ B ] 
# 초기 배치 랜덤
# 정렬 배치 랜덤

#     대 중 소
# 원형 1, 0, 0 (1개)
# 사각 0, 3, 3 (3개)

# 사각
# - 최대 3칸이동, 전기 사용, 칸 이동할때 -y 방향으로 경유하여 이동

# 원형 
# - 짝수팩을 타고 넘어가야됨, 공압 사용, 칸 이동할때 짝수팩의 위로 이동 
# - 타고넘어가는 방향을 화살표로 표시(Hmi)


# [ C ]
# 초기 배치 랜덤
# 정렬 배치 랜덤
# 원형팩을 포함한 가로줄 또는 세로줄 중 한 줄(라인)을 비우고 배치
# 카운트 랜덤(0 ~ 3)

#     대 중 소
# 원형 1, 0, 0 (1개)
# 사각 6, 0, 0 (6개)

# 원형팩을 포함한 가로줄 또는 세로줄 중 한 줄(라인)을 비운상태를 유지하며 정렬
# 팩을 이동시키면 카운트 -1, 라인을 변경하면 카운트 3로 변경
# 카운트가 0이 되면 라인을 무조건 변경 (가로 -> 세로, 세로 -> 가로)
# + 카운트 0이 되기전에 라인을 변경하여도 상관없음. 단, 현재 카운트와 무관하게 카운트는 3로 바꿈

# 라인에 해당하는 칸은 노란색으로 표시(Hmi)


# [ D ]
# 초기 배치 랜덤

#     대 중 소
# 원형 1, 3, 3 (7개)
# 사각 0, 0, 0 (0개)

# t,m1,m2 = 0,'726540310','146053072'  
# t,m1,m2 = 1,'021345670','307541620' 
t,m1,m2,a = 2,'615403702','234567100',2
# t,m1 = 3,'721346500'
    
ts = time()    
if t == 2:
    res = main(t,m1,m2,a)    
elif t == 3:
    res = main(t,m1)
else:
    res = main(t,m1,m2)    
te = time() - ts
if t == 0:
    print('info -> pos,pack,grip,gripper')
print(res)
print("{}step, idle {}s(dart {}m {}s) \n".
format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
