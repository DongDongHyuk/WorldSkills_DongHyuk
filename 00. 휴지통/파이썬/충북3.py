'''
0. algorithm
1. header
2. device communication
 - reading init
 - converting init
 - positions
 - motion
3. main
'''

# 0. Algorithm
def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    step = [e,s] if li == -1 else li
    info = [step,int(m[s])]
    return [''.join(m),info]
    
def aro(pos):
    if pos in cache:
        return cache[pos]
    res = []    
    if t == 2:
        dy,dx = [-1,0,1,0,-1,1,1,-1],[0,1,0,-1,1,1,-1,-1]
    else:
        dy,dx = [-1,0,1,0],[0,1,0,-1]
    y,x = divmod(pos,sx)
    for i in range(8 if t == 2 else 4):
        ny,nx = y + dy[i],x + dx[i]
        if -1 < ny < sy and -1 < nx < sx:
            res.append(ny * sx + nx)
    cache[pos] = res
    return res

def exp(n,m,pos=-1,p:'t == 2'=-1):
    res = []
    for i in range(size) if n > 0 else [pos]:
        if (n > 0 and m[i] != '0') or i in fix:
            continue
        if t == 2 and n > 0 and i in hli:
            continue
        for j in aro(i):
            d = abs(i - j)
            def b(pos1,pos2,d):
                pack = p if p != -1 else m[pos2]
                if pack in (['0x','x'][t == 2] if n > 0 else 'x') or pos2 in fix:
                    return True
                if t == 2:
                    nd = abs(pos1 - pos2)
                    if d in [4,6] and nd not in [4,6] or \
                       d in [1,5] and nd not in [1,5] or \
                       (pack in '1234' and d in [4,6]) or \
                       (pack in '5678' and d in [1,5]):
                        return True
            if b(i,j,d):
                continue            
            if t == 2 and n > 0:
                if j in hli:
                    li = [j]
                    for hp in li:           # hole position                        
                        li0 = [li[0]] + ([] if hp == li[0] else [hp])        # 'li' init state coped                        
                        for k in aro(hp):                            
                            if b(hp,k,d) or k in li:
                                continue                            
                            if m[k] == '0':
                                if k in hli:
                                    li.append(k)
                                continue                            
                            res.append(exc(m,i,k,([i]+li0+[k])[::-1]))                            
                if m[j] == '0':
                    continue                
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def bfs(n,m,*a,p:'t == 2'=-1):
    global res
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    if n == 2:
        leaf,li = a
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
        if n == 2 and all([cur[i] == leaf[i] for i in li]):
            break
        for i,j in exp(n,cur if n > 0 else m,cur,p):
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
    
def sort(m,leaf,e,p=-1):
    res = []
    pack = leaf[e] if p == -1 else p
    if m[e] == pack:
        fix.append(e)
        return m    
    if pack != '0':
        s = m.index(pack)
        if t == 2:
            fix.remove(e)       # 고정컨
            r = bfs(0,m,s,e,p=pack)
            if not (pack in '5678' and e not in [0,4,20,24,5,9,15,19]):
                fix.append(e)
            r = [i for i in r if i not in hli]
        else:
            r = bfs(0,m,s,e)
        for i in r:
            if i in fix:
                fix.remove(i)
            m = bfs(1,m,leaf,i,pack)
    else:
        m = bfs(1,m,leaf,e,'0')
    fix.append(e)
    return m

def main(g_t,m,*a):    
    global t,sy,sx,size,fix,res,cache
    t = g_t
    sy,sx = [[4,4],[4,5],[5,5]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}      # cache reset
    if t == 0:
        pass
    if t == 1:
        leaf = 'x000x0123004560x000x'
        leaf = ''.join(['x' if m[i] == 'x' else leaf[i] for i in range(len(m))])
        m = ['x' if i in [0,4,15,19] else m[i] for i in range(20)]
        leaf = ['x' if i in [0,4,15,19] else leaf[i] for i in range(20)]
        m,leaf = map(''.join,[m,leaf])
        li = []
        n1,n2 = [i for i in [5,10,9,14] if m[i] != 'x']
        for i,j in [n1,1],[n2,-1]:
            m = sort(m,leaf,i,leaf[i+j])
            fix.append(i)
            li.append(i+j)
        li = [i for i in [6,7,8,11,12,13] if i not in li]
        for i in range(1,5):
            m = bfs(2,m,leaf,li[:i])
        fix = li
        m = bfs(1,m,leaf,-1,-1)
    if t == 2:
        global hli
        leaf,hli = a
        hold = []       # 이미 땡긴팩
        unhold = []         # 홀딩 해제 경로
        for pos in range(10):
            fix = [0,1,2,3,4,5,6,7,8,9,10][:pos]
            fix = [i for i in fix if i not in hli]
            # 사용할 수 없는 위치
            if (leaf[pos] == '0' and pos == 0 and leaf[1] in '78' and leaf[5] in '78') or \
               (leaf[pos] == '0' and pos == 4 and leaf[3] in '78' and leaf[9] in '78'):
                m = sort(m,leaf,pos,'0')
                continue            
            if pos in hli :        # 정렬 위치 홀
                continue
            if leaf[pos] == '0' or leaf[pos] in hold:
                li = []
                for i in '12345678':
                    if i not in hold and \
                       i not in ('56' if pos % 2 else '78') and \
                       m.index(i) not in fix:
                        li.append(i)                
                di = {}
                for i in li:
                    li1 = [j for j in '12345678' if i != j and m.index(j) not in fix]
                    fc = fix[:]
                    fix += [leaf.index(j) for j in li1]                    
                    s = leaf.index(i)
                    try:
                        di[i] = [s]+bfs(0,leaf,s,pos,p = i)
                    except:
                        pass
                    fix = fc[:]
                if not di:
                    continue                    
                pack = min(di,key = lambda n:len(di[n]))
                hold.append(pack)
                unhold.append(di[pack][::-1])
            else:
                pack = leaf[pos]
            if pos < 5:
                li = [0,1,2,3,4,20,21,22,23,24][pos:]
            else:
                li = [0,1,2,3,4,5,6,7,8,9][pos:]
            for i in li:
                m = sort(m,leaf,i,'0')
            m = sort(m,leaf,pos,pack)            
        li = [leaf.index(i) for i in '12345678' if m.index(i) not in fix]
        m = bfs(2,m,leaf,li)
        fix += li        
        for r in unhold[::-1]:
            if any([m[i] != '0' for i in r[1:]]):
                print(unhold[::-1],'\n->',r)
                exit()
            m,step = exc(m,r[-1],r[0],r)
            res.append(step)
    return res
# 1. header
tl = lambda *n:tp_log(' '.join(map(str,n)))
from collections import deque
drl_report_line(OFF)
set_tool('tool wei')
set_velx(1000); set_accx(2000)
set_velj([100,150,180,225,225,225]); set_accj(400)
begin_blend(10)
ml,mj,aml,amj,tr,wt = movel,movej,amovel,amovej,trans,wait
def mjx(pos,sol=-1):
    movejx(pos,sol = sol if sol != -1 else (3 if T == 0 else 2))
def rml(x=0,y=0,z=0,a=0,b=0,c=0,t=0.1,vel=None,acc=None):
    aml([x,y,z,a,b,c],mod=1,v=vel,a=acc)
    mwait(0) if t is -1 else wait(t)
def rmj(x=0,y=0,z=0,a=0,b=0,c=0,t=0.1,acc=None):
    amj([x,y,z,a,b,c],mod=1,a=acc)
    mwait(0) if t is -1 else wait(t)
def up(p,mod=0,h=-1):
    p,h = p[:],h if h != -1 else [260,260,260][T]
    p[2] = p[2] + h if mod else h
    return p
tool = 0
def cht(t=0.6,n = -1):
    global tool,pos
    if n != -1 and n == tool:
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
def it(n,t=0.5):
    write(10,n,b=False)
    wt(t * abs(n))
    return 0.5 * abs(n)
gp = 4.5
def gt(n,t=3):
    global gp
    if n == gp:
        return -1
    write(20,n,b=False)
    wt(t *  abs(gp - n))
    n1 = 0.1 * abs(gp - n)
    gp = n
    return n1
        
# 2. device communication
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
    
# - writing init        temp
def writing_init_temp():
    global T
    li1 = [[2, 2, 0, 13, 3, 0, 1, 0, 0, 11, 0, 1, 12, 0, 3, 0], [0, 9, 0, 0, 0, 9, 5, 4, 3, 0, 0, 2, 6, 1, 9, 0, 0, 9, 9, 0], [0, 2, 0, 7, 0, 0, 0, 0, 0, 3, 0, 4, 10, 0, 0, 8, 0, 0, 5, 0, 6, 10, 0, 1, 0]]
    li2 = [None,None,[0, 0, 5, 2, 0, 0, 4, 0, 0, 8, 0, 0, 10, 1, 0, 7, 0, 3, 0, 0, 0, 10, 6, 0, 0]]
    for i in range(3):
        T = i
        write(0,li1[i])
        if i == 2:
            write(len(li1[i]),li2[i])
    write(1,[5,2,0,4,0,1,6,3],b=False)
writing_init_temp()         # temp

# - reading init
root = []
leaf = [-1]*2
info = [-1]*3
for i in range(3):
    T = i
    y,x = [4,4,5][i],[4,5,5][i]
    for j in range(2 if i == 2 else 1):
        m = leaf if j else root
        m.append(read(y * x * j,y,x))
        
# - converting init
def con(m):
    m = ['x' if i == 9 else '0' if i == 10 else str(i) for i in m]
    if T == 1:
        m = ['x' if i in [0,4,15,19] else m[i] for i in range(20)]
    return ''.join(m)
for i in range(3):
    T = i
    root[i] = con(root[i])
    if i == 2:
        info[i] = [j for j in range(25) if leaf[i][j] == 10]
        leaf[i] = con(leaf[i])
       
# - get positions
def ps(pos,y,x,sy=40,sx=40):
    s = y * x
    pos = [pos] * s
    for i in range(1,s):
        if i % x:
            pos[i] = tr(pos[i - 1],[-sx,0,0,0,0,0])
        else:
            pos[i] = tr(pos[i-x],[0,sy,0,0,0,0])
    return pos
poss = [
[None,
ps(posx(33.83, 374.83-40.5, 226.53, 0.1, -90.01, -90.01),4,5),
ps(posx(-226.15, 226.38, 225.01, 0.1, -90.01, -90.01),5,5)],
[None,
None,
ps(posx(-226.73, 384.94-160, 138.4+60, 0.1, -90.01, 89.98),5,5)]]
itp = posx(415.53, 179.38, 291.73, 0.1, 89.99, 90.01)
gtp = [
posx(153.46, 541.33, 247.11, 0.1, -90.01, -90.01),
posx(153.46-360, 541.33, 247.11, 0.1, -90.01, -90.01)]

# - motions
def mt1(p,g,d=[],mod=0,h=-1,z=0,a1=1500,a2=1000,b1=True,b2=False):
    tp = tr(pos[p] if isinstance(p,int) else p,[0,0,-z,0,0,0])
    ml(up(tp,mod,h),a=a1)
    if b2:
        return -1
    ml(tr(tp,[0,0,[-0.15,0][g],0,0,0]),a=a2,r=1)
    grip(g)
    if d:
        ad,val = d
        write(ad,val)
    if b1:
        ml(up(tp),a=a1)

def mt2(pos,g,d=[],mod=0,h=-1,sol=-1):      # index, gantry
    mjx(up(pos,mod,h),sol=sol)
    ml(pos,a=2000)
    if not g:
        wait(0.1)
    grip(g)
    wait(0.1)
    if d:
        ad,val = d
        write(ad,val,b=False)
    ml(up(pos,mod,h))

# 3. Main
def Run():
    if T == 1:      # get the pack in index
        li1 = [6,7,8,11,12,13]
        li2 = [i for i in read(200,4,5,b=False) if i not in [0,9]]
        for i in range(6):
            n = read(1,1,8,b=False).index(li2[i])
            if not i:
                gt(1,0)         # gantry
            it(4 - n)       # index            
            mt2(itp,1,[5,0],1,80,3)
            mt2(gtp[0],0,[],1,80,2)
            gt(2)
            mt2(gtp[1],1,[],1,80,2)
            mt1(li1[i],0,h=300,b1=False)
            if i < 5:
                gt(1,0)         # gantry
            rml(z=200,acc=3000)
    if T == 2:
        mjx(up(pos[20]))
    for i in range(len(res)):
        r = res[i]
        b4 = T == 2 and len(r[0]) > 2
        if b4:
            s,e = r[0][0],r[0][-1]
            road = r[0][1:-1]
        else:
            s,e = r[0]
        p = r[1]       
        af = res[i+1][1] if i < len(res)-1 else -1
        bf = res[i-1][1] if i else -1
        b1,b2 = p == af,p == bf        
        if not b2:
            cht(n = 1 if T == 2 and p in [5,6,7,8] else 0)
            z = [0,10][tool] if T == 2 else 0    # height control
            mt1(s,1,[s,0],z=z,b1=False)
            rml(z=3,acc=300)
        if b4:      # ride hole
            for i in road:
                mt1(i,0,[],1,3,z,b2=True)
        mt1(e,0,[e,p],1,3,z,a2=300,b2=b1)

#write(30,1,b=False)
import time         # temp
time_start = time.time()        # temp

# - Calcurating
#ress = [None]
#for i in range(1,3):
    #tl(i,root[i],leaf[i],info[i])        # temp
    #if info[i] != -1:
        #ress.append(main(i,root[i],leaf[i],info[i]))
    #else:
        #ress.append(main(i,root[i],leaf[i]))
ress = [
None,
[[[11, 10], 2], [[12, 11], 6], [[7, 12], 4], [[11, 16], 6], [[12, 11], 4], [[6, 7], 5], [[11, 6], 4], [[10, 11], 2], [[11, 12], 2], [[6, 11], 4], [[11, 10], 4], [[8, 9], 3], [[7, 2], 5], [[13, 8], 1], [[8, 7], 1], [[7, 6], 1], [[12, 7], 2], [[2, 3], 5], [[3, 8], 5], [[8, 13], 5], [[13, 12], 5], [[7, 2], 2], [[12, 7], 5], [[16, 11], 6], [[11, 12], 6], [[12, 13], 6], [[7, 12], 5], [[2, 7], 2], [[9, 8], 3], [[10, 11], 4]],
[[[1, 2], 2], [[2, 7], 2], [[9, 4], 3], [[3, 9], 7], [[9, 13], 7], [[4, 9], 3], [[20, 16], 6], [[23, 24], 1], [[24, 19], 1], [[11, 6], 4], [[6, 5], 4], [[5, 0], 4], [[7, 6], 2], [[13, 7], 7], [[7, 1], 7], [[18, 14], 5], [[14, 8], 5], [[8, 2], 5], [[6, 7], 2], [[7, 8], 2], [[8, 3], 2], [[16, 12, 8], 6], [[8, 4], 6], [[9, 14], 3], [[14, 13], 3], [[19, 14], 1], [[13, 12, 11], 3], [[14, 13], 1], [[11, 10], 3], [[13, 12, 11], 1], [[15, 21, 17], 8], [[10, 15], 3], [[11, 10], 1], [[10, 5], 1], [[15, 10], 3], [[10, 11], 3], [[11, 6], 3], [[17, 13], 8], [[13, 7], 8], [[7, 13, 9], 8], [[6, 7, 12, 17], 3], [[5, 6, 7, 8, 13], 1], [[4, 8, 14, 18, 22], 6], [[1, 7, 11, 15], 7], [[0, 1, 6], 4]]
]

for i in range(1,3):
    grip(0)
    if i == 1:
        mj([90,0,90,90,90,0])
        tool = 0
    T,pos,res = i,poss[tool][i],ress[i]
    Run()
    
#write(30,1,b=False)
time_end = time.time() - time_start         # temp
minute,second = int(time_end // 60),int(time_end % 60)         # temp
tl('{}m {}s\n'.format(minute,second))         # temp
