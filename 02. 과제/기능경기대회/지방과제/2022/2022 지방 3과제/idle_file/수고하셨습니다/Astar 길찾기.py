import random as r 
printl = lambda li : list(map(lambda a: print(a),li))

def find_road(size_y_x = "none",start = [],arrival = []):
    y_,x_ = map(int,size_y_x.split('x'))
    A = [[9 if x == 0 or y == 0 or x == x_+1 or y == y_+1 else 0 for x in range(x_+2)]for y in range(y_+2)]
    Y = [-1,1,0,0]; X = [0,0,-1,1]; len_save = []; y_save = []; x_save = []; count = 0
    A[arrival[0]][arrival[1]]  = 2 # arrival
    now_y = start[0]; now_x = start[1]
    for i in range(2,6): # random wall spawn
        A[i][r.randint(1,5)] = 9
    printl(A); print("")
    while [now_y,now_x] != arrival and count < 100:
        count += 1
        A[now_y][now_x] = 1 # start
        for i in range(4):
            sum_y = now_y+Y[i]; sum_x = now_x+X[i]
            if A[sum_y][sum_x] == 0:
                len_save.append(abs(arrival[0] - sum_y)+abs(arrival[1] - sum_x)) # len save
                y_save.append(sum_y); x_save.append(sum_x) # y,x save
        for i in range(len(len_save)):
            if len_save[i] == min(len_save):
                now_y = y_save[i]; now_x = x_save[i]
        del len_save[:],y_save[:],x_save[:]
        A[now_y][now_x] = 1 # start        
    printl(A)

find_road("6x4",[1,1],[6,4])



    
    
