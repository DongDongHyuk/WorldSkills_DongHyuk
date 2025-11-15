import random as r
import time as t
A = [[9 if y==0 or x==0 or y==5 or x==7 else 0 for x in range(8)] for y in range(6)]
A[1][3] = A[1][4] = A[4][3] = A[4][4] = 9
li_copy = lambda li : list(map(lambda i : i[:], li))
def start():
    pal = ''
    

def create():
    D = li_copy(A)
    B = [1,2,3,4,5,6,7]
    E = [0,0,0,0,0,0,0,0]
    nul = r.randint(1,8)
    for i in range(6,-1,-1):    
        C = r.randint(0,i)
        for y in range(1,5):
            for x in range(1,3):
                if not D[y][x] and (y-1)*2+x != nul:
                    D[y][x] = B[C]
                    del B[C]
                    break
            else: continue
            E[(y-1)*2+x-1] = D[y][x]
            break
    return [[D],E]
def pal_random():
    O = create()
    for i in O[0]:
        for y in range(1,5):
            for x,x2 in [[1,6],[2,5]]:
                i[y][x2] = O[1][(y-1)*2+x-1]
    Q = O[0][0]
    V = list('00 0000000000000000 00')
    for i in range(len(V)):
        if V[i] == '0':
            for y in range(1,5):
                for x in range(1,7):
                    if Q[y][x] != 9:
                        V[i] = str(Q[y][x])
                        Q[y][x] = 9
                        break
                else: continue
                break
    V = "".join(V)
    return V

