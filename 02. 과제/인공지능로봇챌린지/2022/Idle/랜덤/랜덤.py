import random as r
from algorithm import *

def random_AB():
    A_start = r.randint(0,3)
    A_end = r.randint(0,3)
    A_br1 = ['1','2','3','4']
    A_br6 = ['1','2','3','4']
    r.shuffle(A_br1)
    r.shuffle(A_br6)
    A_br1[A_start] = A_br6[A_end] = '0'
    A_br = ''
    while True:
        well = []
        for _ in range(4):
            well.append(r.randint(0,3))
        if sorted(well) == [0,1,2,3]: continue
        else: break
    r.shuffle(well)
    for i in range(4):
        A_l = ['0','0','0','0']
        A_l[well[i]] = 'x'
        A_br = A_br + "".join(A_l)
    A_br = "".join(A_br1) + A_br + "".join(A_br6)
    index_ = ['0','0','0','0','0','0','0','0']
    i_number = ['1','1','3','3']
    r.shuffle(i_number)
    for i in range(4):
        if r.randint(0,1): index_[i] = i_number[i]
        else: index_[i+4] = i_number[i]
    index_ = "".join(index_)
    A = [0,A_br,index_,A_start,A_end+20]
    #======================================
    bool_B = [ [[1,3],[1,5],[6,10],[8,10],[3,4,5],[6,7,8]],
               [[1,4],[4,9],[2,7],[7,10],[1,5,9],[2,6,10]] ]
    B_peck = []
    B_peck_n = [[1,3],[2,2],[3,1]]
    B_pn = B_peck_n[r.randint(0,2)]
    for i in range(2):
        while 1:
            x = []
            re_bool = 0
            for w in range(B_pn[i]):
                x.append(r.randint(0,11))
            for bool_Bn in bool_B[i]:
                if B_pn[i] < 3:
                    for f in bool_Bn[0:4]:
                        if f == sorted(x):
                            break
                    else: continue
                    break
                else:
                    for f in bool_Bn:
                        if f == sorted(x):
                            break
                    else: continue
                    break
            else:
                if re_bool: continue
                x.append(r.randint(0,11))
                if True in list(map(lambda f: x.count(f) >= 2 ,x)): continue
                B_peck.append([x[:-1],x[-1]])
                break
            break
    B1 = ['0','0','0','0','0','0','0','0','0','0','0','0']
    B2 = ['0','0','0','0','0','0','0','0','0','0','0','0']
    B1_start = []
    B2_start = []
    B_start = [B1_start,B2_start]
    B_all = [B1,B2]
    for i in range(2):
        well,start = B_peck[i]
        B_all[i][start] = '1'
        B_start[i].append(start)
        for t in well:
            B_all[i][t] = 'x'
    for i in range(2):
        while 1:
            pos = r.randint(0,11)
            if B_all[i][pos] == '0' and pos not in B_start[i]:
                B_start[i].append(pos)
            else: continue
            break
    B1 = "".join(B1)
    B2 = "".join(B2)
    e = r.randint(0,3)
    B = [1, [B1,B2],[e,e],[B_start[0][0],B_start[1][0]],[B_start[0][1],B_start[1][1]]]
    return A,B

import time
Max = 0
avg = 0
loop = 0
SUM = 0
while 1:
    start = time.time()
    
    A,B = random_AB()
    result = main(A)
    
    end = time.time() - start
    
    if result[1]:
        if end > Max:
            Max = end
        SUM += end
        loop += 1
        print(A)
        print(result)
        print(loop,'time loops')
        print('Now :',end)
        print('Max :',Max)
        print('avg :',SUM / loop)
        print('\n')

