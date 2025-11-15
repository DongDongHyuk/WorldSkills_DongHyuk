def printl(a,string = "none",count = 1):
    for i in range(9):
        print(a[i], " ") if count % 3 == 0 else print(a[i], end = ' ')
        count += 1
    if string == "": print("")

def find_road(li,start=[],arrival=[]):
    copy_li = li[:]
    li = [[99 if li[y][x] == 9 else 0 for x in range(len(li[0]))]for y in range(len(li))]
    li_ver = len(li)-2 # vertical size
    li_hor = len(li[0])-2 # horizontal size
    count = 1
    li[start[0]][start[1]] = count
    while li[arrival[0]][arrival[1]] != count:
        for y in range(1,li_ver+1):
            for x in range(1,li_hor+1):
                if li[y][x] == count:
                    for i,l in zip([-1,1,0,0],[0,0,-1,1]):
                        if li[y+i][x+l] == 0: li[y+i][x+l] = count +1
        count += 1
    n_y,n_x = arrival[0],arrival[1]
    for i in list(range(count-1,0,-1)):
        li[n_y][n_x] = 1 # 도착 위치 
        for y,x in zip([-1,1,0,0],[0,0,-1,1]): # 상 하 좌 우
            if li[n_y+y][n_x+x] == i and copy_li[n_y+y][n_x+x] == 0: 
                a,b = n_y+y,n_x+x; break
            if li[n_y+y][n_x+x] == i: a,b = n_y+y,n_x+x
        n_y,n_x = a,b
    return list(map(lambda a: list(map(lambda b: 9 if b == 99 else 1 if b == 1 else 0,a)),li))

A = [[9,9,9,9,9,9],
     [9,2,1,2,1,9],
     [9,0,0,9,0,9],
     [9,0,0,0,9,9],
     [9,0,9,0,0,9],
     [9,0,0,9,0,9],
     [9,1,2,1,2,9],
     [9,9,9,9,9,9]]

printl(find_road(A,[1,4],[6,4]))
