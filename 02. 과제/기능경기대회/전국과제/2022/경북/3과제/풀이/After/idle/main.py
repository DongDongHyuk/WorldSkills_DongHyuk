from collections import deque
from printer import *
from time import time

def exc(n,s,e):
    n = list(n)
    n[s],n[e] = n[e],'0'
    return ''.join(n)

def exp(mode,n,pos = None):
    res = []
    li = [i for i in range(len(n)) if n[i] == '0' and i not in fix] if mode else [pos]
    for pos in li:
        if Type != 1:
            for i in range(4):
                npos = pos + dxy[i]
                if pos not in wall[i] and \
                   n[npos] not in (['0','x'] if mode else ['x']) and npos not in fix:
                    res.append(exc(n,pos,npos) if mode else npos)
        else:
            for i in range(4):
                for j in range(2): # floor
                    npos = pos + dxy[i]
                    if j:
                        npos += 9 if pos < 9 else -9
                    if pos not in wall[pos >= 9][i] and \
                       n[npos] not in ['0','x'] and npos not in fix:
                        # 층간 이동 조건
                        if pos >= 9 and n[pos - 9] == '0' or \
                           npos < 9 and n[npos + 9] != '0':
                            continue
                        res.append(exc(n,pos,npos))
    return res

def bfs(mode,n,*args):
    if mode == 0:
        s,e = args
    if mode == 1:
        pos,pack = args
    if mode == 2:
        idx = args[0]
    cur = n if mode else s
    que = deque([cur])
    mkd = {cur:'s'}
    def isleaf(cur):
        if mode == 0 and cur == e or \
           mode == 1 and cur[pos] == pack:
            return 1
        if mode == 2:
            if idx:
                if all([cur[i] == leaf[i] for i in idx]):
                    return 1
            else:
                if cur == leaf:
                    return 1
        return 0
    while 1:
        cur = que.popleft()
        if isleaf(cur):
            break
        for i in exp(mode,cur if mode else n,cur):
            if i not in mkd:
                mkd[i] = cur
                que.append(i)
    mkd['e'] = cur
    return (mkd,cur) if mode else mkd

def path(mkd):
    cur = mkd['e']
    path = [cur]
    while mkd[cur] != 's':
        cur = mkd[cur]
        path.append(cur)
    return path[::-1][1:]

def sort(n,pos):
    res = []
    p = leaf[pos]    
    hold = []    
    cur = pos
    while 1:
        li = exp(0,n,cur)
        if len(li) == 1:
            mkd,n = bfs(1,n,cur,'0')
            res += path(mkd)
            hold.append(cur)
            fix.append(cur)
            cur = li[0]
        else:
            for i in hold:
                fix.remove(i)
            break        
    s = [i for i in range(16) if n[i] == p and i not in fix][0]    
    r = path(bfs(0,n,s,pos))    
    for i in range(len(r)):
        if hold:
            if not i:
                fix.extend(hold)
            if r[i] == r[-len(hold)]:
                for j in hold:
                    fix.remove(j)
        mkd,n = bfs(1,n,r[i],p)
        res += path(mkd)
    fix.append(pos)        
    return res,n

def con(res): # convert
    path = []
    fir = res[0] # first
    for sec in res[1:]:
        step = [None] * 2
        for i in range(len(sec)):
            if fir[i] != sec[i]:
                if fir[i] == '0':
                    step[1] = i
                else:
                    step[0] = i
        path.append(step)
        fir = sec[::]
    return path            

def main(t,r,l):
    global Type,root,leaf,wall,dxy,fix
    Type,root,leaf = t,r,l
    
    res,n = [root],root
    wall = [[[0,1,2],[6,7,8],[0],[8]],
            [[[0,1,2],[2,5,8],[6,7,8],[0,3,6]],
            [[9,10,11],[11,14,17],[15,16,17],[9,12,15]]],
            [[0,1,2,3],[3,7,11,15],[12,13,14,15],[0,4,8,12]]][Type]
    dxy = [[-3,3,-1,1],[-3,1,3,-1],[-4,1,4,-1]][Type]
    fix = []

    if Type == 0:
        for i in [0,8]:
            if leaf[i] != '0':
                mkd,n = bfs(1,n,i,leaf[i])
                res += path(mkd)
                fix.append(i)
        res += path(bfs(2,n,None)[0])

    if Type == 1:
        def aro(pos):
            res = []
            for i in range(4):
                npos = pos + dxy[i]
                if pos not in wall[pos >= 9][i] and npos not in fix:
                    res.append(npos)
            return res        
        for pos in range(9):
            if leaf[pos] != '0':
                fix = [i for i in range(9) if i != pos and n[i] not in ['0',leaf[pos]]]
                mkd,n = bfs(1,n,pos,leaf[pos])
                res += path(mkd)                
        fix = [i for i in range(9) if leaf[i] != '0']
        fp = []
        for pos in range(9):
            if leaf[pos] == '0':                
                for i in aro(pos + 9):
                    if leaf[i] not in ['0','x'] + fp:
                        pack = leaf[i]
                        fp.append(pack)
                        break
                mkd,n = bfs(1,n,pos,pack)
                res += path(mkd)
                fix.append(pos)                
        mkd,n = bfs(2,n,[i for i in range(9,18) if leaf[i] not in fp])
        res += path(mkd)        
        fix.clear()
        res += path(bfs(2,n,None)[0])

    if Type == 2:
        pos = n.index('x')        
        di = {5:wall[3][::]+[3,14,15],9:wall[3][::-1]+[15,2,3],
              6:wall[1][::]+[0,12,13],10:wall[1][::-1]+[12,0,1]}        
        li = [[3,12,15,7,11,13,14],[0,12,15,4,8,13,14],
              [0,3,12,1,2,4,8],[3,12,15,7,11,13,14]]
        if pos in di:
            sqc = di[pos]
        else:
            sqc = [i for i in li if pos not in i][0]
            
        for i in sqc:
            if leaf[i] != '0':
                p,n = sort(n,i)
                res += p
            else:
                mkd,n = bfs(1,n,i,'0')
                res += path(mkd)
                fix.append(i)
        
        res += path(bfs(2,n,None)[0])        

    return res

##Type = 0
##root = '652x41300'
##leaf = '301x24506'

##Type = 1
##root = '13524x006'+'13524x006'
##leaf = '02316x450'+'05643x120'

Type = 2
root = '451203x662041053'
leaf = '150615x642034203'

ts = time()

res = main(Type,root,leaf)

te = time() - ts

for i in res:
    y,x,z = [[1,9,1],[3,3,2],[4,4,1]][Type]
    printf(i,y,x,z)
print('','{} step {}s'.format(len(res),round(te,3)))
print(con(res))
