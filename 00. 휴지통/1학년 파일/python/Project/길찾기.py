A = [[9 if l == 0 or i == 0 or i == 8 or l == 8 else 0 for l in range(9)]for i in range(9)]
for i in A:
    print(i)
def find_road():
    print("===========================")
    count = 1; y = 1; x = 1
    yv = [-1,1,0,0,]; xv = [0,0,1,-1]
    A[1][1] = count 
    while True:
        
        for i in A:
            print(i)
        

find_road()
        
