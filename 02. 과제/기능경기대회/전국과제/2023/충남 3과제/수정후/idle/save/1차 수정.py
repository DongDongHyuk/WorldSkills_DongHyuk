from collections import deque
from time import time
from printer import printf

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    step = [e,s] if li == -1 else li
    pack = 9 if m[s]=='x' else 'abcd'.index(m[s])+11 if m[s].isalpha() else int(m[s])
    info = [step,pack]
    return [(''.join(m),pack) if t == 2 else ''.join(m),info]      
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
    if t == 2:
        m,p = m
    for i in range(size)[(4 if t == 1 else 0):] if n > 0 else [pos]:
        if (n > 0 and m[i] != '0') or i in fix:
            continue
        if t == 1 and (m[i] != '0' or m[i-4] == '0'):
            continue
        if t == 1:
            li = []
            for x in range(4):
                for z in range(4):
                    pos = z * 4 + x
                    if m[pos] == '0' or \
                       (z != 3 and (pos + 4 == i or m[pos+4] != '0')):
                        continue
                    li.append(pos)
                    break
        if t == 2:
            li = [j % 8 for j in [i-3,i-2,i-1,i+1,i+2,i+3]]
        for j in (li if t in [1,2] else aro(i)):
            if (t!=0 and m[j] in ['x','0x'][n > 0]) or j in fix:
                continue
            if t==0:
                if m[j] in ('0' if n>0 else '')+('' if mode==2 else 'x'):
                    continue
                if n<1 and mode==0 and m[j]!='0':
                    continue
            if t == 1:
                di = {4:[13],5:[12,14],6:[13,15],7:[14]}
                ct = 0
                for k in [i,j]:
                    if k in di:
                        for l in di[k]:
                            if m[l] != '0' and not (k == i and l == j):
                                ct = 1
                if ct:
                    continue
            if t == 2 and m[j] == p:
                continue
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res
def bfs(n,m,*a):
    global res
    if n < 1:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n==2:
        li,=a
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        if n==-1 and not que:
            return -1
        cur = que.popleft()
        if n < 1 and cur == e:
            break
        if n == 1:
            cur1 = cur[0] if t == 2 else cur
            if (pos == -1 and cur1 == leaf) or \
               (pos != -1 and cur1[pos] == pack):
                break
        if n==2 and all([cur[i]=='0' for i in li]):
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
    global t,sy,sx,size,fix,res,cache
    t = g_t
    sy,sx = [[4,5],[4,4],[1,8]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}
    if t == 0:
        global mode
        mode=0
        s,e,li=a
        for i in range(5):
            if i==4:
                fix=[j for j in range(20) if m[j]!='0']
                r=bfs(-1,m,s,e)
                if r==-1:
                    fix=[]
                    r=bfs(0,m,s,e)
            else:
                di={}
                for j in li:
                    if j==-1:
                        continue
                    fix=[k for k in li if k!=j]
                    res1=bfs(-1,m,s,j)
                    if res1!=-1:
                        di[j]=res1
                rd=min(di,key=lambda n:len(di[n]))
                r=di[rd]
            r=[s]+r
            if mode:
                fix=[s,e]+li[:]
                for j in range(len(r)):
                    m=bfs(2,m,r[:j])
            if i==4:
                res.append(r)
            else:
                n=li.index(rd)
                li[n]=-1
                door,key=n+1,'abcd'[n]
                pos=m.index(str(door))
                m=''.join(['0' if j==pos else str(key) if j==rd else m[j] for j in range(20)])               
                res.append([r,'abcd'.index(key)+11,[pos,door]])
    if t == 1:
        li, = a
        fix = [0,1,2,3]
        leaf = [m[i] for i in range(4)]+['0']*12        
        for i in range(4):
            pack = leaf[i]
            for j in range(li[i]-1):
                pos = 4 + i + (4 * j)
                leaf[pos] = pack
        leaf = ''.join(leaf)
        for i in range(4,8):
            m = bfs(1,m,leaf,i,leaf[i])
            fix.append(i)
        bfs(1,m,leaf,-1,-1)        
    if t == 2:
        leaf = ['x' if i == 'x' else '0' for i in m]
        pos = 0
        for i in '112233':
            if leaf[pos] == 'x':
                pos += 1
            leaf[pos] = i
            pos += 1
        leaf = ''.join(leaf)
        bfs(1,(m,-1),leaf,-1,-1)
    return res

if __name__ == '__main__':

    ts = time()
    
    t,m,s,e,li= 0,"000x0000x3021040x000",15,4,[0, 10, 19, 17]
    t,m,s,e,li = 0,'000x0240300x00100x00',19,0,[18,1,4,13]
##    t,m,li = 1,'2231321310200000',[2, 2, 3, 3]
##    t,m = 2,'3310122x'      # 인덱스 정렬

    if t == 0:
        res = main(0,m,s,e,li)
    if t == 1:
        res = main(t,m,li)
    if t == 2:
        res = main(t,m)
    
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res) if t != 0 else 'None ',round(te,3),int((te*250)//60),int((te*250)%60)))
