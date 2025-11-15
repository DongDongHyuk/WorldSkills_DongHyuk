import random as R
printl = lambda li: list(map(lambda a: print(a),li))

def find_road(size = "none",start = [],arrival = []):
    size_y,size_x = map(int,size.split("x"))
    A = [[99 if x == 0 or y == 0 or x == size_x+1 or y == size_y+1 else 0 for x in range(size_x + 2)]for y in range(size_y + 2)]
    next_Y = []; next_X = []; err = [-1,1,0,0,0,0,-1,1] # list
    next_Y.append(start[0]); next_X.append(start[1])
    A[start[0]][start[1]] = 1 # 출발 지점 
    point = 1 # int
    for i in range(4):
        A[2+i][R.randrange(1,5)] = 99
    while A[arrival[0]][arrival[1]] == 0: # 숫자 펼치기
        if point == (size_y + size_x) - 1: return -1
        point += 1
        for i in range(len(next_Y)):
            for j in range(4):
                y = next_Y[i] + err[j]; x = next_X[i] + err[4+j]
                if A[y][x] == 0:
                    A[y][x] = point
                    next_Y.append(y); next_X.append(x)
    num = A[arrival[0]][arrival[1]]
    A[arrival[0]][arrival[1]] = 1 # 도착 지점 
    del next_Y[:],next_X[:] # reset
    next_Y = arrival[0]; next_X = arrival[1] # list -> int
    for i in range(num-1,0,-1): # num ~ 0 감소
        for j in range(4):
            y = next_Y + err[j]; x = next_X + err[4+j]
            if A[y][x] == i:
                A[y][x] = 1
                next_Y,next_X = y,x
                break
    A = list(map(lambda a: list(map(lambda b: 1 if b == 1 else 9 if b == 99 else 0,a)),A)) # 길 만들기
    return A

A = find_road("6x4",[1,1],[6,2])
if type(A) == int: print(A)
else: printl(A)
