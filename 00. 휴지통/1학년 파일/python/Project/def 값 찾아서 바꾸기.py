A = [[9 if x == 0 or y == 0 or x == 5 or y == 5 else 0 for x in range(6)]for y in range(6)]
def forYX(a,b,s):
    for y in range(s,a):
        for x in range(s,b):
            yield y,x

A[2][3] = 1         
for y,x in forYX(5,5,1):
    read((y-1)*6+x) == 1
