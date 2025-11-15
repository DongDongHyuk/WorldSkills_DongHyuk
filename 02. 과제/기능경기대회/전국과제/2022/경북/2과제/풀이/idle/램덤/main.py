from collections import deque
from printer import *
import time
import threading

def exc(n,s,e):
    n = list(n)
    pack = n[e]    
    p = pack.lower() == 'p'
    if p:
        m = pack.lower() if pack.isupper() else pack.upper()
        m_p = n.index(m)
        n[s],n[e],n[m_p] = n[e],m,'0'
    else:
        n[s],n[e] = n[e],'0'
    return ''.join(n)
    
def exp(mode,n,pos=None):
    res = []
    dy,dx = [-1,0,1,0],[0,1,0,-1]
    for pos in range(sy*sx) if mode > 0 else [pos]:
        if (mode > 0 and n[pos] != '0') or pos in fix:
            continue
        y,x = divmod(pos,sx)
        for i in range(4):
            ny,nx = y + dy[i],x + dx[i]
            nz = ny * sx + nx
            if  -1 < ny < sy and -1 < nx < sx and \
                n[nz] != 'x' and nz not in fix:
                    res.append(exc(n,pos,nz) if mode > 0 else nz)
    return res

def bfs(mode,n,*args):
    # -1 -> 길이 막혔는지 확인할때
    if mode <= 0:
        pos = args[0]
        s,e = n.index(leaf[pos]),pos
    if mode == 1:
        pos,p,isf = args # 위치, 팩, isFix
        s = n
    if mode == 2:
        s = n
    que = deque([s])
    mkd = {s:'s'}
    while 1:
        if not que or len(mkd) > lm:
            if mode == -1:
                return None
            raise Exception('marked limit' if que else 'que empty')
        cur = que.popleft()        
        if mode <= 0 and cur == e or \
           mode == 2 and cur == leaf:
            break            
        if mode == 1:
            isp = p in ['P','p']
            if isp:
                a,b = leaf.index('P'),leaf.index('p')
                
            def rule(cur,pos):
                def vfix(n,pos):
                    if isp:
                        if n:
                            fix.extend([a,b])
                        else:
                            fix.remove(a)
                            fix.remove(b)
                    else:
                        fix.append(pos) if n else fix.remove(pos)
                vfix(1,pos)
                for i in range(sy*sx):
                    if i not in fix:
                        if bfs(-1,cur,leaf.index(cur[i])) == None:
                            vfix(0,pos)
                            return False
                vfix(0,pos)
                return True
            
            if not isf and cur[pos] == p:
                break            
            if isp:
                if isf and [cur[a],cur[b]] == [leaf[a],leaf[b]] and rule(cur,None):
                    break
            else:
                if isf and cur[pos] == p and rule(cur,pos):
                    break            
        for new in exp(mode,cur if mode > 0 else n,cur):
            if new not in mkd:
                mkd[new] = cur
                que.append(new)
    mkd['e'] = cur
    return (mkd,cur) if mode > 0 else mkd

def path(mkd):
    cur = mkd['e']
    res = [cur]
    while mkd[cur] != 's':
        cur = mkd[cur]
        res.append(cur)
    return res[::-1][1:] if type(cur) == str else res[::-1]

def sort(n,pos):
    res = []
    p = leaf[pos]                   # pos
    r = path(bfs(0,n,pos))          # sorting road
    b = len(exp(0,n,pos)) == 1      # bool
    for i in range(len(r)):
        if b:
            if not i:
                mkd,n = bfs(1,n,pos,'0',False)
                res += path(mkd)
                fix.append(pos)
            if r[i] == r[-1]:
                fix.remove(pos)
        mkd,n = bfs(1,n,r[i],p,r[i] == r[-1])
        res += path(mkd)
    if p not in ['P','p']:
        fix.append(pos)
    else:
        fix.extend([leaf.index('P'),leaf.index('p')])
    
    return res,n

def main(Type,root,l):
    global leaf,sy,sx,fix
    global li,lm
    leaf = l        # leaf node
    sy,sx = [[3,3],[3,4],[3,4],[4,4]][Type]
    fix = []
    res = [root]

    if Type in [0,2]:
        res += path(bfs(2,root,leaf)[0])

    if Type == 1:
        
        n = root
        li = [4,0,8] if n.index('x') == 5 else [7,3,11]

        for i in li:
            p,n = sort(n,i)
            res += p
        res += path(bfs(2,n,leaf)[0])
    
    if Type == 3:
        li = deque([[0,1,4,5],[3,2,7,6],[15,14,11,10],[12,13,8,9]])
        lm,ct = 1000,0

        while res[-1] != leaf:            
            fix = []
            res = [root]
            n = root
            
            try:
                for i in range(4):
                    for j in range(4):
                        pos = li[i][j]
                        if leaf[pos] not in ['x','0']:
                            p,n = sort(n,pos)
                            res += p
                        elif leaf[pos] == '0':
                            mkd,n = bfs(1,n,pos,'0',False)
                            p = path(mkd)
                            res += p
            except:
                li.rotate(1)
                ct += 1
                if not ct % 3:
                    lm *= 2                
    return res

# 3,'0Pp400x603590801','006P80xp93100504'
