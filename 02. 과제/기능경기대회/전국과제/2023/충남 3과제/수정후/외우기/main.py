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
                rd=min(di,key=lambda n:len(di[n]+[j for j in di[n] if m[j]!='0']))
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

from collections import deque
drl_report_line(OFF)
tl = lambda *n:tp_log(' '.join(map(str,n)))
set_tool('tool wei'); set_tcp('tcp')
set_velx(1000); set_accx(2000)
set_velj([100,150,180,225,225,225]); set_accj(400)
begin_blend(10)
ml,mj,aml,amj,tr,wt = movel,movej,amovel,amovej,trans,wait
def mjx(pos,sol=-1):
    movejx(pos,sol = sol if sol != -1 else 2)
def rml(x=0,y=0,z=0,a=0,b=0,c=0,t=0.1,vel=None,acc=None):
    aml([x,y,z,a,b,c],mod=1,v=vel,a=acc)
    wt(t)
def rmj(x=0,y=0,z=0,a=0,b=0,c=0,t=0.1,acc=None):
    amj([x,y,z,a,b,c],mod=1,a=acc)
    wt(t)
def up(pos,mod=0,h=-1):
    pos,h = pos[:],h if h != -1 else 300
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
itli = lambda:read(1,1,8,b=0)
itps = deque([0,1,2,3,4,5,6,7])
def it(n,t=0.6):
    write(10,n,b=0)
    wt(t * abs(n))
    itps.rotate(n)
def gt(n,t=3):
    write(20,n,b=0)
    wt(t)

ser=serial_open('COM')
def ts(ad,m=[],y=0,x=0,b=1):
    if b:
        ad+=100*(T+1)
    k='00'+['R','W'][not y]+'SB06%DW'
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
    wt(0.02 if n == 1 else 0.05)
    k=ser.read(ser.inWaiting())
    if y:
        for i in range(0,y*x*4,4):
            n=int(k[10+i:14+i],16)
            if n&(2**15):
                n-=2**16 
            m.append(n)
        return m if len(m) > 1 else m[0]
def write(*a,b=1):
    if isinstance(a[0],int):
        a = [a]
    for i,j in a:
        ts(i,[j] if isinstance(j,int) else j,b=b)
def read(ad,y=1,x=1,b=1):
    return ts(ad,[],y,x,b=b)
    
root = [-1]*2
info = [-1]*2
for i in range(2):
    T = i
    y,x = [4,4][i],[5,4][i]
    root[i]=read(0,y,x)[:]
        
def con(m):
    m = ['x' if i == 9 else '0' if i > 4 else str(i) for i in m]
    return ''.join(m)
for i in range(2):
    T = i
    if not i:
        li=[]
        for j in range(20)[::-1]:
            if root[i][j]>100:
                li.append(j)
        li1=[]
        for j in [5,6,7,8]:
            li1.append(root[i].index(j))
        li.append(li1)
    else:
        li = read(16,1,4)
    info[i] = li[:]
    root[i] = con(root[i])

def ps(pos,y,x,z=1,sy=40,sx=40,sz=20,err={}):
    s = y * x
    pos = [pos] * (s*z)
    for i in range(1,s*z):
        if not i % s:
            pos[i] = tr(pos[i-s],[0,0,sz,0,0,0])
        elif i % x:
            pos[i] = tr(pos[i - 1],[-sx,0,0,0,0,0])    
        else:
            pos[i] = tr(pos[i-x],[0,sy,0,0,0,0])
        if i in err:
            pos[i]=tr(pos[i],[0,0,err[i],0,0,0])    
    return pos
elcA  = ps(None,4,5)
elcA1 = ps(None,2,2)
airB  = ps(None,1,4,4,sx = 22)
itp = None
gtp = [None,None]
poss = [[elcA,None],[None,airB]]

def mt1(p,g,d=[],mod=0,h=-1,z=0,a1=2000,a2=1500,b1=1,bz=0):
    tp = tr(pos[p] if isinstance(p,int) else p,[0,0,-z,0,0,0])
    ml(up(tp,mod,h),a=a1)
    ml(tp,a=a2,r=5)
    grip(g)
    if bz:
        write(30,bz,b=0)
    if d:
        if isinstance(d[0],int):
            d=[d]
        for i in d:
            ad,val = i
            write(ad,val)
    if b1:
        ml(up(tp),a=a1)

def IT():
    mjx(up(itp,1,70))
    li = itli()
    li = li[4:]+li[0:4]
    for i in range(8):
        if li[i] == 10:
            for j in range(2):
                ml(up(itp,1,[20,10][j]),a=500)
                set_tool_digital_outputs([1,-2])
                wt(0.45)
                isg = not get_tool_digital_input(1)
                pack = [1,2][isg] if j else [0,3][isg]
                b = isg or j
                if b:
                    write(5,pack,b=0)
                grip(0)
                if b:
                    break
        else:
            wt(0.1)
        it(-1)
    wt(1)
    root = ''.join(['x' if i == 9 else str(i) for i in itli()])
    res = main(2,root)
    ml(itp,a=500)
    for i in range(len(res)):
        li = res[i][0]
        p = res[i][1]
        for j in range(2):
            n = 4 - list(itps).index(li[j])
            it(n)
            ml(up(itp,1,[0,5][j]))
            if j:
                rml(z=-5,acc=300)
            grip(not j)
            write(5,[0,p][j],b=0)
            if not j:
                ml(up(itp,1,70))
    it(4 - list(itps).index(4))
    rml(z=60)        
def A():
    global road1
    road1=res[-1]
    mjx(up(elcA1[2]))
    for i in range(len(res)-1):
        r=res[i]
        b1=len(r)>2
        if b1:
            road,key,li=r
            s,e=road[0],road[-1]
            pos2,door=li
            pos1 = read(20,2,2).index(key)            
            mt1(elcA1[pos1],1,[20+pos1,0])
            ml(up(pos[s]))
            for j in road[:-1]:
                ml(up(elcA[j],1,5))
            mt1(e,0,[e,key],1,5,a2=500)
            mt1(pos2,1,[pos2,0])
            mt1(elcA1[pos1],0,[20+pos1,door])            
            continue
        s,e=r[0]
        p=r[1]
        mt1(s,1,[s,0])
        mt1(e,0,[e,p])
def B():
    global road1
    s,e=road1[0],road1[-1]
    m = root[T]
    li = info[T]
    ct = [0,0,0]
    for i in range(4): 
        pack = m[i]
        ct[int(pack)-1] += li[i]
    for i in range(3):
        ct[i] -= m.count(str(i+1))    
    li1 = []
    for i in range(3):
        li1 += [i+1 for j in range(ct[i])]        
    for i in range(4):
        cht(n = 0)
        mjx(up(itp,1,70))
        ml(itp)
        pack = li1[i]
        gt(1,0)
        it(4 - itli().index(pack))
        grip(1)
        write(5,0,b=0)
        rml(z=70)
        mj([90,0,90,90,90,0])
        ml(up(elcA[s]))
        for j in road1:
            ml(up(elcA[j],1,5))
            if j not in [s,e]:
                write(100+j,10,b=0)
                wt(0.05)
                write(100+j,0,b=0)
        rml(z=70)
        mj([90,0,90,90,90,0])
        mt1(gtp[0],0,[],b1=0)
        wt(1)
        set_tcp('tcp1')
        rml(b=-45,acc=300,t=0.5)
        grip(1)
        rml(z=50)
        rml(b=90,acc=300,t=1)
        rml(z=-70,t=0.5)
        grip(0)
        rml(z=70,t=1)
        set_tcp('tcp')
        gt(2)
        cht()
        mt1(gtp[1],1,[])
        pos = [j for j in range(i,16,4) if m[j] == '0'][0]
        mt1(pos,0,[pos,pack])
        m = ''.join([str(pack) if j == pos else m[j] for j in range(16)])
    res = main(1,m,li)
    cht(n = 1)
    for i in range(len(res)):
        r = res[i]
        s,e = r[0]
        p = r[1]
        mt1(s,1,[[s,0],[20,p]],bz=2)
        mt1(e,0,[[e,p],[20,0]])
        
write(30,5,b=0)
s,e,li=info[0]
ress=[main(0,root[0],s,e,li),None]
grip(0)
IT()
for i in range(2):
    T,pos,res = i,poss[tool][i],ress[i]
    Run = [A,B][i]
    Run()
write(30,5,b=0)