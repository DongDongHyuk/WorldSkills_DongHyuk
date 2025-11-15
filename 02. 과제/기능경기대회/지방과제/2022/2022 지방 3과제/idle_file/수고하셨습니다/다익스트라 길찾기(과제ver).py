printl = lambda li: list(map(lambda a: print(a),li))

def find_road(li,start = [],arrival = []):
    A = list(map(lambda a: list(map(lambda b:99 if b == 9 else 0,a)),li))
    return A
    next_Y = []; next_X = []; err = [-1,1,0,0,0,0,-1,1]+[0,88] # list
    next_Y.append(start[0]); next_X.append(start[1]) # 출발 지점
    A[start[0]][start[1]] = 1 # 출발 지점
    A[arrival[0]][arrival[1]] = 0 # 도착 지점
    point = 1 #int
    while A[arrival[0]][arrival[1]] == 0: # 숫자 펼치기
        point += 1
        len_save = len(next_Y)
        for i in range(len_save):
            for j in range(4):
                y = next_Y[i] + err[j]; x = next_X[i] + err[4+j]
                if A[y][x] == 88 or A[y][x] == 0:
                    A[y][x] = point
                    next_Y.append(y); next_X.append(x)
        del next_Y[:len_save],next_X[:len_save]
    num = A[arrival[0]][arrival[1]]
    A[arrival[0]][arrival[1]] = 1 # 도착 지점 
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

li0 = [[9,9,9,9,9,9],
       [9,2,2,1,1,9],
       [9,0,0,9,0,9],
       [9,0,0,0,9,9],
       [9,0,9,0,0,9],
       [9,0,0,9,0,9],
       [9,1,2,1,2,9],
       [9,9,9,9,9,9]]

for y in range(4):
    for x in range(4):
        print([1,1+y],[6,1+x])
        printl(find_road(li0,[1,1+y],[6,1+x]))
        print("")
