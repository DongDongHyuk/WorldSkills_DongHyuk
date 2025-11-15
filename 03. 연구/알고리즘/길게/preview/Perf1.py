from time import time
from Tool.Printer import prt

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    r = [e,s] if li == -1 else li
    info = [r,10+'abc'.index(m[s]) if m[s] in 'abc' else int(m[s])]
    return [''.join(m),info]

def aro(p):
    dxy = [-sx,1,sx,-1]
    li = [[(0,1,2,3),(3,7,11,15),(12,13,14,15),(0,4,8,12)],[],[]][t]
    return [p + dxy[i] for i in range(4) if p not in li[i]]

def exp(n,m,p=-1):
    res = []
    for i in range(size) if n > 0 else [p]:
        if (n > 0 and m[i] != '0') or fx[i]:
            continue
        for j in [j for j in aro(i) if m[j] not in ['x','0x'][n > 0] and not fx[j]]:            
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def src(n,m,*a):
    global res,mkdCt        # temp
    if n == 0:
        s,e = a
    if n == 1:
        p,pk = a
    q = [m if n > 0 else s] 
    mkd = {i:[] for i in q}
    while 1:
        if n == 0 and not q:        # temp
            return -1
        cur = q.pop(0)
        if n > 0:       # temp
            mkdCt += 1
        if n == 0 and cur == e:
            break
        if n == 1:
            if (pk == -1 and cur == p) or (p != -1 and cur[p] == pk):
                break
        for i,j in exp(n,cur if n > 0 else m,cur):
            if i not in mkd:
                q.append(i)
                mkd[i] = mkd[cur] + [i]
    path = mkd[cur]
    if n > 0:
        res += path
        return cur
    return path
    
def sort(m,e,pk):

    r = [e]
    while m[e] != pk:
        li = exp(0,m,e)
        if len(li) > 1:
            break
        m = src(1,m,e,'0')
        fx[e] = 1
        e = li[0][0]
        r.append(e)

    while m[e] != pk:
        s = m.index(pk)
        p = src(0,m,s,e)[0]
        fx[s] = 1

        r1 = []         # '0'이 p로 이동하는 경로
        for i in range(size):
            if m[i] == '0':
                r2 = src(0,m,i,p)
                if r2 != -1 and (not r1 or r1 > r2):
                    r1 = r2[:]

        print('p : {}, pk : {}'.format(e,pk))
        print('fx ->',[i for i in fx if fx[i]])
        print('r1 ->',r1)
        prt(m,4,4)

        # fuck = [i for i in range(size) if m[i] != 'x' and not fx[i] and not exp(0,m,i)]
        # if fuck:
        #     print('fuck ->',fuck)
        #     exit()

        if not r1:
            exit(print('hold shit'))

        for i in r1:
            m = src(1,m,i,'0')
        fx[s] = 0
        m = src(1,m,p,pk)

    if len(r) > 1:
        s = r[0]
        m,r = exc(m,s,e,r[::-1])
        res.append(r)
        fx[s],fx[e] = 1,0
    else:
        fx[e] =  1
    return m

def main(g_t,m,*a):
    global t,sy,sx,size,fx,fxli,res
    t = g_t
    sy,sx = [[4,4],[0,0],[0,0]][t]
    size = sy * sx
    fx = {i:0 for i in range(size)}         # temp(dict)
    fxli = lambda li,n: fx.update({i:n for i in li})
    res = []
    if t == 0:
        leaf, = a        
        for i in [0]:
            m = sort(m,i,leaf[i])
    return res

mkdCt = 0       # temp
if __name__ == '__main__':

    t = 0
    m1 = ['0','0','0','b',
          'a','9','8','x',
          '7','6','5','4',
          'x','3','2','1']
    m2 = ['1','2','3','4',
          '5','6','7','x',
          '8','9','a','b',
          'x','0','0','0']
    m1,m2 = map(''.join,[m1,m2])

    '''
    00 01 02 03
    04 05 06 07
    08 09 10 11 
    12 13 14 15
    '''

    # t,m1,m2 = 0,'000cbxa987654321','12345x6789abc000'

    ts = time()    
    res = main(t,m1,m2)
    te = time() - ts
    # for i in res:
    #     if type(i) == str: 
    #         prt(i,4,4)
    #     else:
    #         print(i)
    # print(res)
    print('visited :',mkdCt)
    te *= 3.5      # temp
    print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))