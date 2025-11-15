li_copy = lambda li : list(map(lambda f : f[:],li))
# C-1 (목표 노드), C-3 파레트의 다음 노드(간선이 이어진 노드), g_score
def mirror_mode(pal, count = 0,m_pal = [0] * 9):
    for i in [3,2,1,6,5,4,9,8,7]:
        m_pal[count] = pal[i-1]
        count += 1
    return m_pal

def astar(goal,now_state,g=0):
    print("C-3(goal) : {}".format(goal))
    print("C-1(state): {}".format(now_state))
    goal = [[9 if x==0 or y==0 or x==4 or y==4 else goal[((y-1)*3+x)-1] for x in range(5)]for y in range(5)]
    now_state = [[9 if x==0 or y==0 or x==4 or y==4 else now_state[((y-1)*3+x)-1] for x in range(5)]for y in range(5)]
    print(" ")
    
    # 추정거리 계산
    def Manhattan_D(start_y,start_x,arrival_y,arrival_x):
        return abs(arrival_x-start_x)+abs(arrival_y-start_y)
    
    #h(x) = 모든 팩의 추정거리 합
    def h_(val):
        for y in range(1,4):
            for x in range(1,4):
                if goal[y][x] != now_state[y][x]:
                    start = [y,x] # 출발 좌표                   
                    # 숫자 펼치기로 찾기 
                    box = li_copy(now_state) # 리스트 복사
                    yv = [0] * 15; xv = [0] * 15
                    yv[0] = start[0]; xv[0] = start[1] # 출발 지점
                    yl = [-1,1,0,0]; xl = [0,0,-1,1] # 상 하 좌 우
                    count = 0; stop = 0; find_val = now_state[start[0]][start[1]]
                    print("찾는 값: {}".format(find_val)) 
                    while stop == 0:
                        for i in range(4):
                            a = yv[0]+yl[i]; b = xv[0]+xl[i]
                            now_state[yv[0]][xv[0]] = -1
                            if goal[a][b] == find_val:
                                arrival = [a,b] # 도착 좌표
                                val += Manhattan_D(start[0],start[1],arrival[0],arrival[1])
                                print("출발 좌표: {}".format(start)); print("도착 좌표: {}".format(arrival)) 
                                return val
                            elif now_state[a][b] != 9 and now_state[a][b] != -1:
                                count+=1
                                yv[count] = a; xv[count] = b
                            if now_state[a][b] != 9: now_state[a][b] = -1
                        for l in range(7):
                            yv[l] = yv[l+1] # 리스트 밀기 
                            xv[l] = xv[l+1]
                        count -=1  
    h = h_(0)
    print("f({}) = g({}) + h({})".format(g+h,g,h))

astar(mirror_mode([2,2,1,0,1,2,3,1,0]),[1,2,2,2,1,1,0,0,3],0)
