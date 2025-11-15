def exc(m,s,e=-1,g=-1,p=-1,gli=-1):
    m = list(m)
    if g != -1:
        isg = g == 1
        pack = m[s] if isg else p
        gp = gli.index('0' if isg else p)
        gli = list(gli)
        gli[gp] = pack if isg else '0'
        m[s] = '0' if isg else p
    else:
        m[s],m[e] = m[e],m[s]
        pack = m[s]
        if t == 0:
            gp = gli.index('0')
    pack = ('abc'.index(pack)+10 if pack.isalpha() else int(pack)) + [0,12,18,24][t]
    info = [s,g,pack,gp] if g != -1 else [[e,s],pack]
    if t == 0 and g == -1:
        info.append(gp)
    return [(''.join(m),tuple(gli)) if t == 0 else ''.join(m), info]    
def aro(pos):
    if pos in cache:
        return cache[pos]
    res = []
    if t == 2:
        di = {1:3,3:1,6:8,8:6,11:13,13:11}
        if pos in di:
            res = [di[pos]]
    dy,dx = [-1,0,1,0]*3,[0,1,0,-1]*3
    dz = [-1,-1,-1,-1,0,0,0,0,1,1,1,1]
    y,x,z = (pos // sx) % sy, pos % sx, pos // size
    for i in range(12):
        ny,nx,nz = y + dy[i],x + dx[i],z + dz[i]
        if -1 < ny < sy and -1 < nx < sx and -1 < nz < sz:
            n = ny * sx + nx + (size * nz)
            res.append(n)
    cache[pos] = res
    return res
def exp(n,m,pos=-1,pack=-1):
    if t == 0:
        m,gli = m
    res = []
    for i in range(size * sz) if n > 0 else [pos]:
        if i in fix:
            continue
        if t == 0:
            if m[i] == '0' and gli.count('0') < 2 and (i > 5 or m[i + 6] == '0') and (i < 6 or m[i - 6] != '0'):
                for p in gli:
                    if p != '0':                        
                        res.append(exc(m,i,g=0,p=p,gli=gli))
            if gli.count('0') < 1:
                continue
            if m[i] != '0' and (i > 5 or m[i + 6] == '0'):
                res.append(exc(m,i,g=1,gli=gli))
        if n > 0 and m[i] != '0':
            continue
        if t == 2:
            if i in [2,7,12]:
                continue
        for j in [j for j in aro(i) if m[j] not in ['x','0x'][n > 0] and j not in fix]:            
            if t == 0:
                if (i > 5 and m[i - 6] == '0') or (j < 6 and m[j + 6] != '0'):
                    continue
            if t == 2:
                if abs(i - j) == 2: 
                    h, = [k for k in hli if (k - 1) in [i,j]]
                    if any([(m[j] if n > 0 else pack) in st and h != hli[k] for k,st in enumerate(['14','25','36'])]):
                        continue
            res.append(exc(m,i,j,gli = gli if t == 0 else -1) if n > 0 else [j,j])
    return res
def bfs(n,m,*a):
    global res
    runM = m[1] if t == 3 and len(m) == 2 else -1
    if runM != -1:
        m = m[0]
    if n == 0:
        if t == 2:
            s,e,pack = a
        else:
            s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 2:
        pos,pack1,pack2 = a
    if n == 3:
        li,ct = a
    if n == 4:
        leaf,li,ct = a
    if n == 5:
        pos,li = a
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n == 0 and cur == e:
            break
        if n == 1:
            cur1 = cur[0] if t == 0 else cur
            if (pos == -1 and cur1 == leaf) or (pos != -1 and cur1[pos] == pack):
                break
        if n == 2 and (pos == -1 or cur[0][pos] == pack1) and pack2 in cur[1]:
            break
        if n == 3 and [cur[i] for i in li].count('0') == ct:
            break
        if n == 4 and [cur[i] == leaf[i] for i in li].count(1) >= ct:
            break
        if n == 5 and cur[pos] in li:
            break
        for i,j in exp(n,(cur if n > 0 else m),(cur if n < 1 else -1),(pack if n < 1 and t == 2 else -1)):
            if i not in mkd:
                que.append(i)
                mkd[i],step[i] = cur,([runM] + j if runM != -1 else j)
    mkd[-2] = cur
    path = [step[cur]]
    while mkd[cur] != -1:
        cur = mkd[cur]
        path.append(step[cur])
    if n > 0:
        res += path[::-1][1:]
        return mkd[-2]
    return path[::-1][1:]    
def sort(m,leaf,e,p=-1):
    pack = leaf[e] if p == -1 else p
    if t == 3:
        m,j = m
    s = m.index(pack)
    if t == 2:
        r = bfs(0,m,s,e,pack)
    else:
        r = bfs(0,m,s,e)        
    for i in r:
        m = bfs(1,(m,j) if t == 3 else m,leaf,i,pack)
    fix.append(e)
    return m
def main(g_t,m,*a):    
    global t,sy,sx,sz,size,fix,res,cache
    t = g_t
    sy,sx,sz = [[1,6,2],[3,3,1],[3,5,1],[3,3,1]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}
    if t == 0:
        m = (m,('0','0'))
        leaf = '123456cba987'
        for i in [0,6,1,7,2,8,3,9,4,10]:
            pack = leaf[i]
            m = bfs(2,m,-1,-1,pack)
            for j in range(i, -1, -6):
                if j not in fix:
                    m = bfs(2,m,j,'0',pack)
            m = bfs(1,m,leaf,i,pack)
            fix.append(i)
        m = bfs(1,m,leaf,-1,-1)        
    if t == 1:
        leaf = '123456000'
        for i in range(6):
            m = sort(m,leaf,i,leaf[i])
    if t == 2:
        global hli
        hli, = a
        leaf = '01040x205x03060'
        li = [0,10,1]
        for i in range(1,4):
            m = bfs(3,m,li,i)
        fix = [10]
        m = sort(m,leaf,0,'1')
        fix = [0]
        li = [3,6,8,11,13]
        for i in range(1,6):
            m = bfs(4,m,leaf,li,i)
        fix = []
        m = bfs(1,m,leaf,-1,-1)
    if t == 3:
        m2, = a
        m1 = m[:]
        leaf1,leaf2 = '123456000','0a70b80c9'
        red = [5,1]
        blue = [7,3]
        for i in range(6 - len([i for i in m1 if i in '123456'])):
            for j in range(2):
                mc1,mc2 = [m1,m2][j][:],[m2,m1][j][:]
                h1,h2 = red[1] if j else blue[0],red[0] if j else blue[1]
                mc1 = bfs(5,(mc1,j),h1,'123456' if j else '789abc')
                mc2 = bfs(1,(mc2,(1 - j)),None,h2,'0')
                mc1,mc2 = map(list,[mc1,mc2])
                mc1[h1],mc2[h2] = mc2[h2],mc1[h1]
                mc1,mc2 = map(''.join,[mc1,mc2])
                m1,m2 = [mc1,mc2][j][:],[mc2,mc1][j][:]
                pack = ('abc'.index(mc2[h2])+10 if mc2[h2].isalpha() else int(mc2[h2])) + [0,12,18,24][t]
                res.append([j,pack]) 
        for j in range(2):
            m,leaf = [m1,m2][j][:],[leaf1,leaf2][j][:]
            fix = []
            for i in [2,5,8,1,4,7] if j else range(6):
                m = sort((m,j),leaf,i,leaf[i])
    return res

tl = lambda *n:tp_log(' '.join(map(str,n)))
from collections import deque
drl_report_line(OFF)
set_tool('tool wei')
set_velx(1000); set_accx(2000)
set_velj([100,150,180,225,225,225]); set_accj(400)
begin_blend(10)
ml,mj,aml,amj,tr,wt = movel,movej,amovel,amovej,trans,wait
def mjx(pos,sol=-1):
    movejx(pos,sol= sol if sol != -1 else 2)
def rml(x=0,y=0,z=0,a=0,b=0,c=0,t=0.1,vel=None,acc=None):
    aml([x,y,z,a,b,c],mod=1,v=vel,a=acc)
    mwait(0) if t is -1 else wait(t)
def rmj(x=0,y=0,z=0,a=0,b=0,c=0,t=0.1,acc=None):
    amj([x,y,z,a,b,c],mod=1,acc=acc)
    mwait(0) if t is -1 else wait(t)
def up(p,mod=0,h=-1):
    p,h = p[:],h if h != -1 else [400,280,280,280][T]
    p[2] = p[2] + h if mod else h
    return p
tool = 0
def cht(t=0.6,n = -1):
    global tool,pos
    if n == tool:
        return -1
    tool = (1 - tool)
    rmj(c=-180 if tool else 180,t=t,acc=1500)
    pos = poss[tool][T]
isgrip = False
def grip(n):
    global isgrip
    isgrip = n
    if tool:
        if not n:
            wt(0.1)
        write(40,n,b=False)
        wt(0.15)
    else:
        set_tool_digital_outputs([1,-2] if n else [-1,2])
        wt(0.25)

ser=serial_open("COM")
def ts(ad,m=[],y=0,x=0,b=True):
    if b:
        ad += 100 * (1 + T)
    k='00'+['W','R'][bool(y)]+'SB06%DW'
    k=[ord(i) for i in k]
    n=len(m) if not y else y*x
    ad = [0]*(3-len(str(ad))) + list(map(int,str(ad)))
    k+=[ord(str(abs(i))) for i in ad]
    k+=[ord(i) for i in '{:02X}'.format(n)]
    if not y:
        for i in m:
            if i<0:
                i+=2**16
            k+=[ord(j) for j in '{:04X}'.format(i)]
    ser.write([5]+k+[4])
    wait(0.02 if n is 1 else 0.05)
    k=ser.read(ser.inWaiting())
    if y:
        for i in range(0,y*x*4,4):
            v=int(k[10+i:14+i],16)
            if v&(1<<15):
                v-=2**16 
            m.append(v)
        return m if len(m) > 1 else m[0]
def write(*a,b = True):
    if isinstance(a[0],int):
        a = [a]
    for i,j in a:
        ts(i,j if isinstance(j,list) else [j],b=b)
def read(ad,y=1,x=1,b=True):
    return ts(ad,[],y,x,b=b)

root = [-1] * 4
init = [-1] *4
for i in range(4):
    T = i
    y,x = [2,3,3,3][i],[6,3,5,6][i]
    root[i] = read(0,y,x)[:]
init[2] = [root[2].index(i) for i in range(1,4)]

def con(t,m):
    if t == 2:
        m = [0 if i < 4 else i for i in m]
    m = [m[i] - [0,12,18,24][t] if m[i] > 0 else m[i] for i in range(len(m))]
    m = [chr(i+87) if i > 9 else str(i) for i in m]
    if t == 2:
        m = ['x' if i in [5,9] else m[i] for i in range(15)]
    return ''.join(m)
for i in range(4):
    root[i] = con(i,root[i])
    
def ps(pos,y,x,z,li):
    a = y * x
    s = y * x * z
    dy1,dx1,dy2,dx2 = li
    pos = [pos] * s
    for i in range(1,s):
        if not i % a:
            pos[i] = trans(pos[i-a],[0,0,60,0,0,0])
        elif i % x:
            pos[i] = trans(pos[i-1],[dy1,dx1,0,0,0,0])
        else:
            pos[i] = trans(pos[i-x],[dy2,dx2,0,0,0,0])
    return pos
elcA = ps(posx(437.65, 479.22, 231.78, 169.85, -90, -90), 1,6,2,[-7,-39,0,0])
elcB = ps(posx(225.23, 428.16, 228.48, 169.85, -90, -90), 3,3,1,[-39,7,7,39])
elcC = ps(posx(-302.28, 354.19, 228.34, 164.87, 90, 90), 3,5,1,[-38.5,10.5,10.5,38.5])
elcD1 = ps(posx(102.12, 473.84, 228.85, 134.73, 90, 90), 3,3,1,[-28.5,-28.5,-28.5,28.5])
elcD2 = ps(posx(-47.97, 474.89, 228.79, 134.81, 90, 90), 3,3,1,[-28.5,-28.5,-28.5,28.5])       
airA = ps(posx(438.91, 480.36, 138.65+60, 170.09, -90.02, 89.97), 1,6,2,[-7,-39,0,0])
airB = ps(posx(226.15, 428.75, 137.2+60, 170.1, -90.01, 89.95), 3,3,1,[-39,7,7,39])
airC = ps(posx(-302.51, 352.76, 136.62+60, 164.98, 90, -90), 3,5,1,[-38.5,10.5,10.5,38.5])
airD = [[posx(16.36, 501.75, 137.62+60, 134.25, 90, -90),
         posx(-29.02, 547.84, 138.21+60, 134.98, 90, -90),
         posx(-77.13, 502.18, 136.91+60, 134.32, 90, -90)],
        [posx(-77.12, 445.88, 137.77+60, 134.79, 90, -90),
         posx(-29.52, 399, 137.33+60, 134.78, 90, -90),
         posx(15.89, 445.58, 136.94+60, 134.69, 90, -90)]]
poss = [[elcA,elcB,elcC,[elcD1,elcD2]],[airA,airB,airC,None]]

def mt1(p,g,d=[],mod=0,h=-1,z=0,b1=True,b2=False,a1=2000,a2=1000,dt=-1):
    tp = tr((pos[dt][p] if dt != -1 else pos[p]) if type(p) == int else p,[0,0,-z,0,0,0])    
    ml(up(tp,mod,h),a=a1)
    if b2:
        return -1
    ml(tp,a=a2,r = 5)
    if not g:
        rml(z=-0.15,acc = 300)
    grip(g)
    if d:
        ad,val = d
        write(ad + (0 if dt == -1 else [0,9][dt]),val)
    if b1:
        ml(up(tp))        

def pz(p):
    li1 = [[1,2,7,8],[13,16],[19,22],[25,26,31,32]][T]
    li2 = [[3,4,9,10],[14,17],[20,23],[27,28,33,34]][T]
    return 20 if p in li1 else 10 if p in li2 else 0
def RunA():
    def getz(pos,g,p,gp):
        z = sum([pz(read(j)) for j in range(pos % 6, pos, 6)])
        z += pz(read(pos) if g else p) if gp == 1 else 0
        return z    
    for i in res:
        if len(i) == 3:
            li,p,gp = i
            s,e = li
            cht(n = gp)
            mt1(s,1,[s,0],z = getz(s,1,p,gp),a2=2500)
            mt1(e,0,[e,p],z = getz(e,0,p,gp),a2=2500)
        else:
            s,g,p,gp = i    
            cht(n = gp)
            mt1(s,g,[s,0 if g else p],z = getz(s,g,p,gp),a2=2500)            
def RunBCD():
    cht(n = 0)
    for i,j in enumerate(res):
        if T == 3:
            if len(j) == 2:
                dt,p = j       
                a,b,c = [airD[dt][i] for i in range(3)]
                s,e = [1,5] if dt else [7,3]  
                z = pz(p)
                cht(n = 1)
                mt1(a,1,[s,0],z=z,b1=0,dt=dt)
                rml(z=3,acc=800)
                mt1(b,0,None,1,3,z=z,b2=1)
                mt1(c,0,[e,p],1,3,z=z,dt=not dt)
                cht(n = 0)
                continue
            dt,li,p = j
        else:
            li,p = j
            dt = -1
        s,e = li
        if T == 1:
            b1,b2 = 0,0
        elif T == 3:
            a = res[i-1][2] if i and len(res[i-1]) > 2 else -1
            b = res[i+1][2] if i < len(res)-1 and len(res[i+1]) > 2 else -1
            b1,b2 = p == b,p == a
        else:
            a = res[i-1][1] if i else -1
            b = res[i+1][1] if i < len(res)-1 else -1
            b1,b2 = p == b,p == a
        if T == 1:
            cht(n = 4 in [s,e]) 
        if T == 2:
            cht(n = p > 21)       
        z = pz(p) if tool == 1 else 0
        if not b2:
            mt1(s,1,[s,0],z=z,b1=0,dt=dt)
            rml(z=3,acc=800)
        mt1(e,0,[e,p],1,3,z=z,b2=b1,dt=dt)

write(30,1,b=False)
ress = []
for i in range(4):
    if i == 2:
        ress.append(main(i,root[i],init[i]))
    elif i == 3:
        ress.append(main(i,root[i][:9],root[i][9:]))
    else:
        ress.append(main(i,root[i]))     
for i in [0,1,3,2]:
    grip(0)
    if i in [0,3]:
        if i == 3:
            rml(z = 100)
        amj([90,0,90,90,-90 if i == 0 else 90,0])
        wait(0.2 if i else 0.5)
        tool = 0
    T,pos,res = i,poss[tool][i],ress[i]
    Run = [RunA,RunBCD,RunBCD,RunBCD][i]
    Run()    
write(30,1,b=False)