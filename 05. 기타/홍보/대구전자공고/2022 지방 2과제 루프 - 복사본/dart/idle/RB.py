import random

def prt(li: list):
    li = ''.join(map(str,li))
    print("",li[:3])
    print("",li[3:6])
    print("",li[6:])
    print("-----")

def random_pal():
    mr = lambda li: [li[i-1] for i in [3,2,1,6,5,4,9,8,7]]
    A_2 = [1,2,3,1,2,3]
    C_1 = [0]*9
    C_3 = C_1[:]
    random.shuffle(A_2)
    C_1[random.randint(0,8)] = 3
    C_3 = mr(C_1)
    num_li =  [[1,1,1,2,2,2],[1,2]]
    Cs = [C_1,C_3]
    for j in num_li:
        C = Cs[num_li.index(j)]
        for i in j:
            while 1:
                pos = random.randint(0,8)
                if not C[pos]: break
            C[pos] = i
    return A_2,C_1,C_3

result = random_pal()
print(result[0])
print("-----")
prt(result[1])
prt(result[2])
    
