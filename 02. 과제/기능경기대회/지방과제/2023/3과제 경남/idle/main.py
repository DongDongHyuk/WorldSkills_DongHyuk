from collections import deque

def exc(m,s,e):
    m = list(m)
    m[s],m[e] = m[e],'0'
    return ''.join(m)

def exp(m):
    res = []
    li = [i for i in range(8) if m[i] == '0' and i not in fix]
    for pos in li:
        for npos in range(8):
            if m[npos] != '0' and npos not in fix + [pos]:
                res.append(exc(m,pos,npos))
    return res

def bfs(m,pos):
    que = deque([m])
    mkd = {m:'s'}
    while 1:
        cur = que.popleft()
        if cur[pos] == leaf[pos]:
            break
        for  i in exp(cur):
            if i not in mkd:
                mkd[i] = cur
                que.append(i)
    mkd['e'] = cur
    return mkd,cur

def path(mkd):
    cur = mkd['e']
    path = [cur]
    while mkd[cur] != 's':
        cur = mkd[cur]
        path.append(cur)
    return path[::-1][1:]

def con(res):
    path = []
    fir = res[0]
    for sec in res[1:]:
        step = [None] * 2
        for i in range(8):
            if fir[i] != sec[i]:
                if fir[i] == '0':
                    step[1] = i
                else:
                    step[0] = i
        path.append(step)
        fir = sec[:]
    return path

def main(m,tf = False):
    global leaf,fix
    leaf = m[:]
    leaf.sort()
    leaf = leaf[::-1] if tf else leaf[2:]+[0,0]
    sqc = [i for i in leaf if i != 0]
    cvt = lambda li: ''.join(['0' if i == 0 else str(sqc.index(i)+1) for i in li])
    m,leaf = map(cvt,[m,leaf])
    res = [m] 
    fix = [i for i in range(6) if m[i] == leaf[i]]   
    for i in range(6):
        mkd,m = bfs(m,i)
        res += path(mkd)
        fix.append(i)
    return con(res)
