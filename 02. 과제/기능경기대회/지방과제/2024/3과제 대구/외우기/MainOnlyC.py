def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    step = [e,s] if li == -1 else li
    info = []
    for i in li:
        pack = 'abc'.index(i[1])+10 if i[1].isalpha() else int(i[1])
        info.append([i[0],pack])
        for j in i[0]:
            m[j] = '0'
    for i in li:
        li1,pack = i[0],i[1]
        m[li1[1]] = pack
    return [''.join(m),info]
def exp(n,m,pos=-1):
    res = []
    for i in range(10) if n > 0 else [pos]:
        ct = 1+i
        ct_ = 0
        for j in range(9-i):
            res1 = []
            for k in range(ct):
                for l in range(0,20,10):
                    if m[j+k+l] != '0':
                        pos1 = j+k+l
                    if m[ct-k+j+l] != '0':
                            pos2 = ct-k+j+l
                if pos1 in fix or pos2 in fix:
                    ct_ = 1
                    continue
                pos3,pos4 = pos2,pos1
                if (pos1 < 10 and pos2 < 10) or (pos1 > 9 and pos2 > 9):
                    pos3 = pos2+10 if pos1 < 10 else pos2-10
                    pos4 = pos1+10 if pos1 < 10 else pos1-10
                if pos1 == pos2:
                    res1.append([[pos1,pos3],m[pos1]])
                    break
                else:
                    res1.append([[pos1,pos3],m[pos1]])
                    res1.append([[pos2,pos4],m[pos2]])
                    if (ct == 3 and k == 1) or (ct == 5 and k == 2) or \
                        (ct == 7 and k == 3) or (ct == 9 and k == 4) or ct == 1:
                        break
            if ct_ != 0:
                ct_ = 0
                continue
            res.append(exc(m,-1,-1,res1))
        if i == 9:
            return res
        continue
    return res
def bfs(n,m,*a):
    global res
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 3:
        pack,li = a
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
        if n == 3:
            if ''.join([cur[i] for i in li]) == pack:
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
    global t,fix,res,cache
    t = g_t
    fix = []
    res = []
    cache = {}      # cache reset
    leaf, = a
    for i in range(5):
        for j in range(0,20,10):
            if leaf[i+j] != '0' and leaf[i+j] != m[i+j]:
                m = bfs(1,m,leaf,i+j,leaf[i+j])
        pos = i+j-10 if i+j > 9 else i+j+10
        fix += [i+j,pos]
    li = []
    pack = []
    for i in range(5,10):
        for j in range(0,20,10):
            if leaf[i+j] != '0':
                li.append(i+j)
                pack.append(leaf[i+j])
    pack = ''.join(pack)
    for i in range(1,len(li)+1):
        m = bfs(3,m,pack[:i],li[:i])
    res1 = []
    for i in res:
        res1 += i
    res = res1
    return res
    
tl = lambda *n:tp_log(' '.join(map(str,n)))
from collections import deque
drl_report_line(OFF)
set_tool('tool wei')
set_velx(1500); set_accx(2500)
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
    p,h = p[:],h if h != -1 else 300
    p[2] = p[2] + h if mod else h
    return p
tool = 0
def cht(t=0.6,n = -1):
    global tool,pos
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
    return ts(ad,[],y,x,b)

y,x = 2,10
root = read(0,y,x)[:]
leaf = read(y*x+10,y,x)[:]

def con(m):
    m = ['a' if i == 10 else str(i) for i in m]
    return ''.join(m)
root = con(root)
leaf = con(leaf)
    
def ps(pos,y,x,sy=40,sx=40):
    s = y * x 
    pos = [pos] * s
    for i in range(1,s):
        if i % x:
            pos[i] = trans(pos[i-1],[-sx,0,0,0,0,0])
        else:
            pos[i] = trans(pos[i-x],[0,sy,0,0,0,0])
    return pos
elcC = ps(posx(-128.82, 322.19, 228.09, 0.13, -90, -89.96),3,10)
airC = ps(posx(-130.62, 323.24, 136.35+60, 0.37, -90.02, 90.05),3,10)
poss = [[None,None,elcC],[None,None,airC]]

def mt1(p,g,d=[],mod=0,h=-1,z=0,a1=1800,a2=1000):
    tp = tr(pos[p] if type(p) == int else p,[0,0,z,0,0,0])      
    ml(up(tp,mod,h),a=a1)
    ml(tp,a=a2,r = 15)
    if not g:
        rml(z=-0.15,acc = 300)
    grip(g)
    if d:
        ad,val = d
        write(ad,val)
    ml(up(tp),r = 15)

def RunC():
    i = 0
    while i < len(res):    
        step,p = res[i]    
        areaLen = abs((step[0] % 10) - (step[1] % 10)) + 1        
        li = res[i:i+areaLen]       # 내림차춘으로 변경
        li.sort(key = lambda n : n[0][0] % 10)        
        C3 = []
        for j in range(2):    
            cht()
            for n in range(areaLen):
                step,p = li[n]
                s,e = step                
                if not j and s < 10:        # C1 -> C3
                    z = -(20 if p < 4 else 10 if p < 9 else 0)
                    mt1(s,1,[s,0],z=z)
                    mt1(e+10,0,[e+10,p],z=z)                    
                    C3.append([e+10,p])                    
                if j and p not in [k[1] for k in C3]:       # C2 -> C1
                    mt1(s,1,[s,0])
                    mt1(e,0,[e,p])                             
        C3.sort(key = lambda n : n[0] % 10)       # 내림차춘으로 변경
        for j in range(len(C3)):        # C3 -> C2
            s,p = C3[j]
            e = s - 10
            mt1(s,1,[s,0])
            mt1(e,0,[e,p])            
        i += areaLen

write(30,1,b=False)
grip(0)
mj([90,0,90,90,90,0])
tool = 0
T,pos,res = 2,poss[tool][2],main(2,root,leaf)
RunC()
write(30,1,b=False)