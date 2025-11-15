now_state = [1,2,2,2,1,0,1,0,3];
now_state = [[9 if x==0 or y==0 or x==4 or y==4 else now_state[((y-1)*3+x)-1] for x in range(5)]for y in range(5)]
li_copy = lambda li : list(map(lambda f : f[:],li))
box = li_copy(now_state)
yv = [0] * 15; xv = [0] * 15
yl = [-1,1,0,0]; xl = [0,0,-1,1]
yv[0] = 1; xv[0] = 1
count = 0; stop = 0; find_val = 3
while stop == 0:
    for i in range(4):
        a = yv[0]+yl[i]; b = xv[0]+xl[i]    
        now_state[yv[0]][xv[0]] = -1
        if now_state[a][b] == find_val:
            stop = 1
        elif now_state[a][b] != 9 and now_state[a][b] != -1:
            count+=1
            yv[count] = a; xv[count] = b
        if now_state[a][b] != 9: now_state[a][b] = -1
    for l in range(7):
        yv[l] = yv[l+1] # 리스트 밀기 
        xv[l] = xv[l+1]
    count -=1

