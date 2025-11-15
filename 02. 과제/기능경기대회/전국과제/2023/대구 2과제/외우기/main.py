def exc(m,s,e,li,g=-1,p=-1):
    m = list(m)
    li = list(li) if t < 3 else -1
    con = lambda n: ord(n)-87 if ord(n) > 96 else int(n)
    if g != -1:
        m[s] = '0' if g else p
        li.append(p) if g else li.remove(p)
        return [(''.join(m),tuple(li)),[s,g,con(p),e]]
    m[s],m[e] = m[e],m[s]
    if t == 1 and m[s] == 'b':
        step = [e,s]
        m[e],m[e+(e-s)] = 'b','0'
        n = [i+sx for i in range(sx) if m[i+sx] != '0']
        if n:
            n, = n
            n1,n2 = n+(s-e),n
            m[n1],m[n2] = m[n2],'0'
        if m[s+sx] != '0':
            step = [e+(e-s),e]
        step.append(m.index('b'))
        step += [n2,n1,con(m[n1])] if n else [-1]*3
    else:
        if t == 2:
            li=[-1,1] if li==[-3,3] else [-3,3]
            step = [e,s,con(m[e]),con(m[s])]
        else:
            step = [e,s,con(m[s])]
    return [(''.join(m),tuple(li)) if t < 3 else ''.join(m),step]
def aro(pos):
    if pos in cache:
        return cache[pos]
    res = []
    dy,dx = [[0,0,0,0]*5,[-3,-1,1,3]*5] if t == 1 else [[-1,0,1,0]*5,[0,1,0,-1]*5]
    dz = [-2,-2,-2,-2,-1,-1,-1,-1,0,0,0,0,1,1,1,1,2,2,2,2]
    y,x,z = (pos // sx) % sy, pos % sx, pos // size
    for i in range(20):
        ny,nx,nz = y + dy[i],x + dx[i],z + dz[i]
        if -1 < ny < sy and -1 < nx < sx and -1 < nz < sz:
            n = ny * sx + nx + (size * nz)
            res.append(n)
    cache[pos] = res
    return res
def exp(n,m,pos=-1):
    res = []
    if t < 3:
        m,li = m
    for i in range(size*sz) if n else [pos]:        
        if t == 0 and m[i] != '0' and len(li) < 2 and (i > 3 or m[i+2] == '0'):            
                res.append(exc(m,i,-1,li,1,m[i]))
        if t == 0 and m[i] == '0' and li and (i > 3 or m[i+2] == '0') and (i < 2 or m[i-2] != '0'):
            for j in li:
                res.append(exc(m,i,-1,li,0,j))                
        if ((n and m[i] != '0') and t not in [1,2]) or i in fix:
            continue        
        for j in [j for j in aro(i) if m[j] not in ['x','0x'][n > 0] and j not in fix]:
            if t == 0 and len(li) == 2:
                continue            
            if t == 0 or (t == 3 and n):
                if (i >= size and m[i - size] == '0') or (j < size*(sz-1) and m[j + size] != '0'):
                        continue
            if t == 1:
                d = abs(i-j)
                if d == 1 and m[j] == 'b' and m[i] not in '0b' and len(li) < 1:
                    res.append(exc(m,i,-1,li,1,m[i]))                    
                if m[i] != '0':
                    continue
                if d == 1 and m[j] == 'b' and m[j+sx] == '0' and li:
                    for k in li:
                        res.append(exc(m,i,j,li,0,k))             
                b1 = (m[j] in '135' and any([k in '135' for k in li])) or \
                     (m[j] in '246' and any([k in '246' for k in li]))
                b2 = d in [sx-3,sx+3]
                b3 = m[j] == 'b' and m[sx:].count('0') < sx-1
                b4 = d == 3 and (m[j] == 'b' or m[i+((j-i)//3)] != 'b' or m[sx:].count('0') < sx)
                b5 = i >= sx and (m[i - sx] != 'b' or m[j] == 'b')
                if any([b1,b2,b3,b4,b5]):
                    continue
            if t == 2 and i-j not in li:
                continue                        
            res.append(exc(m,i,j,li if t < 3 else -1) if n else [j,j])            
    return res
def bfs(n,m,*a):
    global res
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 2:
        li, = a
    cur = m if n else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n == 0 and cur == e:
            break
        if n == 1:
            cur1,li = cur if t < 3 else (cur,-1)
            if cur1 == leaf or \
               (pos != -1 and cur1[pos] == pack and (t != 1 or not li)):
                    break
        if n == 2 and all([cur[i] == '0' for i in li]):
            break
        for i,j in exp(n,cur if n else m,cur):
            if i not in mkd:
                que.append(i)
                mkd[i],step[i] = cur,j
    mkd[-2] = cur
    path = [step[cur]]
    while mkd[cur] != -1:
        cur = mkd[cur]
        path.append(step[cur])
    if n:
        res += path[::-1][1:]
        return mkd[-2]
    return path[::-1][1:]
def sort(m,leaf,e):
    pack = leaf[e]
    s = m.index(pack)
    road = [s]+bfs(0,m,s,e)
    for i in range(len(road)):
        n = road[i]
        if t == 3 and n < 18:            
            if i:
                fix.append(road[i-1])
                fix.append(road[i-1]+9)
            li = [j for j in range(n,27,9) if j != s][::-1]
            for j in range(4):
                m = bfs(2,m,li[:j])
            if i:
                del fix[-2:]
        m = bfs(1,m,leaf,n,pack)    
    fix.append(e)
    return m
def main(g_t,m,*a):    
    global t,sy,sx,sz,size,fix,res,cache
    t = g_t
    sy,sx,sz = [[1,2,3],[1,7,2],[3,3,1],[3,3,3]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}
    if t == 0:
        m,leaf = (m,()),'142530'
        bfs(1,m,leaf,-1,-1)
    if t == 1:
        m,leaf = (m,()),'1234bb00000000'
        for i in range(7):
            m = bfs(1,m,leaf,i,leaf[i])
            fix.append(i)
    if t == 2:
        m,leaf = (m,(-1,1)),'123456789'
        for i in range(3):
            m = bfs(1,m,leaf,i,leaf[i])
            fix.append(i)
        bfs(1,m,leaf,-1,-1)
    if t == 3:
        leaf, = a
        for i in range(18):
            if leaf[i] != '0':
                m = sort(m,leaf,i)
        for i in range(3):
            for j in range(i,27,9):
                if j not in fix:
                    m = bfs(1,m,leaf,j,leaf[j])
                    fix.append(j)
        bfs(1,m,leaf,-1,-1)
    return res

from collections import deque
drl_report_line(OFF)
tl = lambda *n:tp_log(' '.join(map(str,n)))
set_tool('tool wei')
set_velx(1000); set_accx(2000)
set_velj([100,150,180,225,225,225]); set_accj(400)
begin_blend(10)
ml,mj,aml,amj,tr,wt = movel,movej,amovel,amovej,trans,wait
def mjx(pos,sol=-1):
    movejx(pos,sol=sol if sol != -1 else (2 if T==3 else 3))
def rml(x=0,y=0,z=0,a=0,b=0,c=0,t=0.1,vel=None,acc=None):
    aml([x,y,z,a,b,c],mod=1,v=vel,a=acc)
    wt(t)
def rmj(x=0,y=0,z=0,a=0,b=0,c=0,t=0.1,acc=None):
    amj([x,y,z,a,b,c],mod=1,a=acc)
    wt(t)
def up(pos,mod=0,h=-1):
    pos,h = pos[:],h if h != -1 else [400,300,300,400][T]
    pos[2] = pos[2] + h if mod else h
    return pos
tool = 0
def cht(t=0.6,n = -1):
    global tool,pos
    if n == tool:
        return -1
    tool = (1 - tool)
    rmj(c=-180 if tool else 180,t=t,acc=1500)
    pos = poss[tool][T]
isgrip = 0
def grip(n):
    global isgrip
    isgrip = n
    if tool:
        if not n:
            wt(0.1)
        write(40,n,b=0)
    else:
        set_tool_digital_outputs([1,-2] if n else [-1,2])
    wt(0.25)

ser = serial_open('COM')
def ts(ad,m=[],y=0,x=0,b=1):
    if b:
        ad+=100*(T+1)
    k='00'+['R','W'][not y]+'SB06%DW'
    k=[ord(i) for i in k]
    n = len(m) if not y else y * x
    ad = [0]*(3-len(str(ad)))+list(map(int,str(ad)))
    k+=[ord(str(abs(i))) for i in ad]
    k+=[ord(i) for i in '{:02X}'.format(n)]
    if not y:
        for i in m:
            if i<0:
                i+=2**16
            k+=[ord(j) for j in '{:04X}'.format(i)]
    ser.write([5]+k+[4])
    wt(0.02 if n == 1 else 0.05)
    k=ser.read(ser.inWaiting())
    if y:
        for i in range(0,y*x*4,4):
            n = int(k[10+i:14+i],16)
            if n&(2**15):
                n-=2**16
            m.append(n)
        return m if len(m) > 1 else m[0]
def write(*a,b = 1):
    if isinstance(a[0],int):
        a = [a]
    for i,j in a:
        ts(i,[j] if isinstance(j,int) else j,b=b)
def read(ad,y=1,x=1,b=1):
    return ts(ad,[],y,x,b=b)

root = [-1] * 4  
leaf = [-1] * 4
for i in range(4):
    T = i
    y,x = [2,7,3,9][i],[3,2,3,3][i]
    for j in range(2 if i == 3 else 1):
        m = read(y*x*j,y,x)[:]
        if j:
            leaf[i] = m[:]
        else:
            root[i] = m[:]
        
def con(m):
    if i == 1:
        n = m.index(5)
        m[n],m[n+1]= 'b','b'
    if i == 3:
        m = [chr(j+87) if j > 9 else j for j in m]
    return ''.join(map(str,m))
for i in range(4):
    root[i] = con(root[i])
    if i == 3:
        leaf[i] = con(leaf[i])

def ps(pos,y,x,z,sy=40,sx=40,sz=60,err={}):
    s = y * x    
    pos = [pos] * (s*z)
    for i in range(1,s*z):
        if not i % s:
            pos[i] = tr(pos[i-s],[0,0,sz,0,0,0])
        elif i % x:
            pos[i] = tr(pos[i-1],[-sx,0,0,0,0,0])
        else:
            pos[i] = tr(pos[i-x],[0,sy,0,0,0,0])
        if i in err:
            pos[i] = tr(pos[i],[0,0,err[i],0,0,0])
    return pos
elcA = ps(None,1,2,3,0,80,40)
elcB = ps(None,1,7,2)
elcC = ps(None,3,3,1)
elcD = ps(None,3,3,3,80,80)
airA = ps(None,1,2,3,0,80,40)
airB = ps(None,1,7,2)
airC = ps(None,3,3,1)
poss = [[elcA,elcB,elcC,elcD],[airA,airB,airC,None]]

def mt1(p,g,d=[],mod=0,h=-1,z=0,a1=2000,a2=1000,b1=1):
    b2 = T!=1 and not g and tool
    if T == 1 and p > 6:
        z += 40
    tp = tr(pos[p],[0,0,[0,3][b2]-z,0,0,0])    
    ml(up(tp,mod,h),a=a1)
    ml(tp,a=a2,r = 5)
    if b2:
        rml(z=-3,acc=300)
    grip(g)
    if d:
        if isinstance(d[0],int):
            d = [d]
        for i in d:
            if i != -1:
                ad,val = i
                write(ad,val)
    if b1:
        ml(up(tp))

def AB(r):
    global gli
    s,g,p,bp = r
    d = [s,0 if g else p]
    if not g and tool not in gli:
        cht()
    if T == 1 and g and ((not tool and p in [1,3]) or (tool and p in [2,4])):
        cht()
    if bp != -1:
        ml(up(pos[bp]))
        ml(up(pos[bp],1,25))
        mt1(s,0,d,1,25,a1 = 500)
    else:
        mt1(s,g,d)
    if g:
        gli[tool] = p
    else:
        del gli[tool]        
def A():
    global gli
    mjx(up(pos[1]))
    gli = {}
    for i in range(len(res)):
        r = res[i]
        if tool in gli:
            cht()
        if len(r) == 4:
            AB(r)
        else:
            s,e,p = r
            mt1(s,1,[s,0])
            mt1(e,0,[e,p])
def C():
    mjx(up(pos[4]))
    cht(n = 0)
    for i in range(len(res)):
        s,e,a,b = res[i]
        write(9,2 if i % 2 else 1)
        for j in range(2):
            mt1(s,not j,[s,a if j else 0],z = 10 if j and a < 5 else 0)
            cht()
            mt1(e,not j,[e,b if j else 0],z = 10 if not j and a < 5 else 0)
def D():
    rml(z=100)
    mjx(up(pos[3]))
    def ph(pos):
        p = pack if pos in [s,e] else read(pos)
        return 20 if p < 5 else 10 if p < 10 else 0
    for i in range(len(res)):
        s,e,pack = res[i]
        sf,ef = s//9+1,e//9+1
        write([54,[sf,ef]],[s,20+pack],[e,20])
        for j in range(2):
            pos1 = [s,e][j]
            z = sum(map(ph,range(pos1%9,pos1,9)))
            mt1(pos1,not j,[pos1,[0,pack][j]+20],z=z,a2=2000)
        write([s,0],[e,pack])
def B():
    global gli
    rmj(90)
    mjx(up(pos[0],h=400))
    gli = {}
    for i in range(len(res)):
        r = res[i]
        if  len(r) == 4:
            AB(r)
        else:
            if len(r) == 6:
                if tool in gli:
                    cht()
                s,e,bp,a,b,p = r
                z = [15,20][tool]
                b1 = a != -1
                d = [[read(0,1,7).index(5),0],[a,0] if b1 else -1]
                mt1(s,1,d,z=z,b1=0)
                d = [[bp,5],[b,p] if b1 else -1]
                mt1(e,0,d,1,0,z,500)
            else:
                s,e,p = r
                if (not tool and p in [1,3]) or (tool and p in [2,4]):
                    cht()
                mt1(s,1,[s,0])
                mt1(e,0,[e,p])

write(30,1,b=0)
ress = []
for i in range(4):
    if i == 3:
        ress.append(main(i,root[i],leaf[i]))
    else:
        ress.append(main(i,root[i]))    
for i in [0,2,3,1]:
    grip(0) 
    T,pos,res = i,poss[tool][i],ress[i]
    Run = [A,B,C,D][i]
    Run()
write(30,1,b=0)