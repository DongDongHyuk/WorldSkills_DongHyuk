def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    info = [[e,s] if li == -1 else li,int(m[s])]
    return [''.join(m), info]    
def aro(pos):
    if pos in cache:
        return cache[pos]
    di = [{3:[16,19], 4:[20,23],
           16:[3,32], 19:[3], 20:[4], 23:[4,39],
           32:[16,51], 35:[51], 36:[52], 39:[23,52],
           51:[32,35],52:[36,39]},
          {0:[6], 4:[8],
           6:[0], 8:[4],
           16:[20], 18:[24],
           20:[16], 24:[18]},
           None][t]
    res = di[pos] if pos in di else []
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
    for i in range(size * sz) if n > 0 else [pos]:
        if (n > 0 and m[i] != '0') or i in fix:
            continue
        if t == 0 and n > 0 and i in hli:
            continue
        for j in range(15) if t == 2 else aro(i):            
            b = lambda j: m[j] in 'x' or j in fix
            if b(j):
                continue
            if t == 0 and n > 0 and j in hli:
                que = deque([j])
                mkd = {j:i,i:-1}
                while que:
                    cur = que.popleft()
                    for k in aro(cur):
                        if k not in mkd:                                
                            mkd[k] = cur
                            if k in hli:
                                que.append(k)
                            if m[k] == '0' or b(k):
                                continue
                            res1 = path(mkd,mkd,k)+[k]
                            res.append(exc(m,i,k,li=res1[::-1]))
            if n > 0 and m[j] == '0':
                continue     
            if t == 0 and n > 0:
                for k in res:
                    _,step = k
                    step = step[0]
                    if [j,i] == [step[0],step[-1]]:
                        res.remove(k)
            if t == 1 and n > 0:
                if i in red and m[j] not in '123' or i in blue and m[j] not in '4567':
                   continue            
            if t == 2:
                if (i > 4 and (m[i - 5] == '0' or i - 5 == j)) or (j < 10 and m[j + 5] != '0'):
                    continue
                if m[j] in '123':
                    if i not in [[0,1,2,3,4],[5,6,7,8,9],[10,11,12,13,14]][int(m[j])-1]:
                        continue
                    a,b = sorted([i,j])
                    if any([i != '0' for i in m[a+1:b]]):
                        continue
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res
def bfs(n,m,*a):
    global res
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 2:
        li, = a
    if n == 3:
        li1,li2,ct1,ct2 = a
    if n == 4:
        pack, = a
    cur =  m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n == 0 and cur == e:
            break
        if n == 1:
            cur1 = cur
            if (pos == -1 and cur1 == leaf) or (pos != -1 and cur1[pos] == pack):
                break            
        if n == 2 and [cur[i] for i in li].count('0') < 2:
            break
        if n == 3:
            count1,count2 = 0,0
            li3,li4 = map(lambda li:[cur[i] for i in li],[li1,li2])
            if n == 3:
                for i in range(4):
                    pack = li3[i]
                    if pack != '0':
                        count1 += 1 if pack in li4 else 0
                        count2 += 1 if pack == li4[i] else 0
            if count1 >= ct1 and count2 >= ct2:
                break
        if n == 4:
            pos = cur.index(pack)
            if pos > 9 or cur[pos + 5] == '0':
                break
        for i,j in exp(n,cur if n > 0 else m,cur):
            if i not in mkd:
                que.append(i)
                mkd[i],step[i] = cur,j
    res1 = path(mkd,step,cur)    
    if n > 0:
        res += res1
        return cur
    return res1
def path(mkd,step,cur):
    path = [step[cur]]
    while mkd[cur] != -1:
        cur = mkd[cur]
        path.append(step[cur])
    return path[::-1][1:]    
def sort(m,leaf,e,p=-1):
    global fix
    pack = leaf[e] if p == -1 else p
    s = [i for i in range(size) if m[i] == pack and i not in fix][0]
    r = bfs(0,m,s,e)
    for i in r:
        if t == 0 and i in hli:
            continue
        m = bfs(1,m,leaf,i,pack)
    fix.append(e)
    return m
def main(g_t,m,*a):    
    global t,sy,sx,sz,size,fix,res,cache
    t = g_t
    sy,sx,sz = [[7,8,1],[5,5,1],[1,5,3]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}
    if t == 0:
        global hli
        hli, = a
        li = [[18,21],[26,29],[27,28]] if m[19] == 'x' else [[34,37],[26,29],[27,28]]
        li = [i for i in li if i != hli]
        for li in li:
            m = bfs(2,m,li)
            pos = [i for i in li if m[i] != '0'][0]
            pack = m[pos]
            for i in li:
                if m[i] == pack:
                    fix.append(i)
                else:
                    m = sort(m,None,i,pack)
        li1,li2 = [3,16,32,51],[4,23,39,52]
        for i in range(1,5):
            m = bfs(3,m,li1,li2,i,0)
        for i in range(1,5):
            m = bfs(3,m,li1,li2,0,i)
    if t == 2:
        leaf, = a
        li = [[4,3,2,1],[0,4,3,2],[0,4,1,3],[4,0,1,2],[0,1,2,3]]
        for pos in li[leaf.index('1')]:
            pack = leaf[pos]
            for i in range(10+pos,pos-1,-5):
                m = bfs(1,m,leaf,i,'0')
            fix.append(pos)
            m = bfs(4,m,pack)
            i,j = pos,m.index(pack)
            m,step = exc(m,i,j)    
            res.append(step)
        fix = [0,1,2,3,4]
        m = bfs(1,m,leaf,-1,-1)
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
    p,h = p[:],h if h != -1 else [280,300,450][T]
    p[2] = p[2] + h if mod else h
    return p
tool = 0
def cht(t=0.6,n = -1):
    global tool,pos
    if n == tool:
        return -1
    tool = (1 - tool)
    rmj(c=180 if tool else -180,t=t,acc=1500)
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

root = [-1] * 3
leaf = [-1] * 3
init = [-1] * 3
for i in range(3):
    T = i
    y,x = [7,5,3][i],[8,5,5][i]
    root[i] = read(0,y,x)[:]
    if i:
        leaf[i] = read(y*x,y,x)[:]
init[0] = [i for i in range(56) if root[0][i] == 10]
init[1] = [[],[]]
for i in range(25):
    n = root[1][i]
    if n > 9:
        init[1][n > 19].append(i)

def con(t,m):
    li = [[0,1,2,5,6,7,8,9,10,11,12,13,14,15,17,22,24,25,30,31,33,38,40,41,42,43,44,45,46,47,48,49,50,53,54,55],
          [1,3,5,9,12,15,19,21,23],
          None][t]
    m = ['x' if t < 2 and (i in li or m[i] == 9) else '0' if m[i] > 9 else str(m[i]) for i in range(len(m))]
    return ''.join(m)
for i in range(3):
    root[i] = con(i,root[i])       
    if i:
        leaf[i] = con(i,leaf[i])

def ps(pos,y,x,z,sy=40,sx=40,sz=60):
    a = y * x
    s = y * x * z
    pos = [pos] * s
    for i in range(1,s):
        if not i % a:
            pos[i] = trans(pos[i-a],[0,0,sz,0,0,0])
        elif i % x:
            pos[i] = trans(pos[i-1],[-sx,0,0,0,0,0])
        else:
            pos[i] = trans(pos[i-x],[0,sy,0,0,0,0])
    return pos
elcA = ps(posx(110.48, 407.07-80, 229.92, 179.76, -90, -90.01),7,8,1)
elcB = None
elcC = ps(posx(-274.37, 288.13, 228.83, 89.84, 90.02, 89.97),1,5,3)
airA = ps(posx(111.04, 408.1-80, 135.98+60, 0.39, 90, -90),7,8,1)
airB = None
airC = ps(posx(-275.49, 288.7, 135.66+60, 90.15, 90, -90),1,5,3)
poss = [[elcA,elcB,elcC],[airA,airB,airC]]

def mt1(p,g,d=[],mod=0,h=-1,z=0,b1=True,b2=False,a1=2000,a2=1000):
    tp = tr(pos[p] if type(p) == int else p,[0,0,-z,0,0,0])    
    ml(up(tp,mod,h),a=a1)
    if b2:
        return -1
    ml(tp,a=a2,r = 5)
    if not g:
        rml(z=-0.15,acc = 300)
    grip(g)
    if d:
        ad,val = d
        write(ad,val)
    if b1:
        ml(up(tp))

def RunAC():
    pz = lambda p:10 if p < 7 else 0
    def getz(pos,p,gp):
        z = sum([pz(read(j)) for j in range(pos % 5, pos, 5)])
        z += pz(p) if gp else 0
        return z        
    for i in range(len(res)):
        li,p = res[i]
        if len(li) > 2:
            s,e = li[0],li[-1]
        else:
            s,e = li        
        if T == 0:
            gp,gap = p > 3,3
            a = [res[i-1][1],res[i-1][0][-1]] if i else -1
            b = [res[i+1][1],res[i+1][0][0]] if i < len(res)-1 else -1
            b1,b2 = [p,e] == b,[p,s] == a
            z1,z2 = [20 if gp else 0]*2
            a1,a2 = 800,1000            
        if T == 2:
            gp,gap = p < 4,30
            b1,b2 = 0,0
            z1,z2 = getz(s,p,gp),getz(e,p,gp)
            a1,a2 = 1250,2500            
        cht(n = gp)        
        if T == 2 and p > 3:
            mt1(s,1,[s,0],z = z1,a2=a2)
            mt1(e,0,[e,p],z = z2,a2=a2)
            continue
        if not b2:
            mt1(s,1,[s,0],z=z1,b1=0,a1=2500,a2=a2)
            rml(z=gap,acc=a1)
        if len(li) > 2:
            for i in li[1:-1]:
                mt1(i,1,[],1,gap,z=z1,b2=1)                
        mt1(e,0,[e,p],1,gap,z=z2,b2=b1,a2=a1)

write(30,1,b=False)
ress = []
for i in range(3):
    if i == 0:        
        ress.append(main(i,root[i],init[i]))
    if i == 1:
        ress.append(None)
    if i == 2:
        ress.append(main(i,root[i],leaf[i]))
for i in [0,2]:
    grip(0)
    if i in [0,2]:
        if i == 2:
            rml(z = 100)
        amj([160 if i else 90,0,90,90,-90,0])
        wait(0.5 if i else 0.8)
        tool = 0
    T,pos,res = i,poss[tool][i],ress[i]
    Run = [RunAC,None,RunAC][i]
    Run()
write(30,1,b=False)