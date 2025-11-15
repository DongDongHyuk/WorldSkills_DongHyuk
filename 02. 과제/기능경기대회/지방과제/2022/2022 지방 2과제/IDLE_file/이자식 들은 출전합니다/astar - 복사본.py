F = []; br_box = []; br_box_2 = []; recode = [] # list
g = 1 # int
    
goal_br = [1,1,1,
           2,2,2,
           3,0,0]
br= [1,2,3,
     2,1,0,
     2,0,1]

def recoding_board(): 
    global br,recode
    re_id = br[:] # id가 겹쳐서 re_id를 겹침
    recode.append(re_id) # 노드를 저장함
    
def comparing_board(): 
    start = [0] * 2; arrival = [0] * 2; length = [];
    y = [1,1,1,2,2,2,3,3,3]; x = [1,2,3,1,2,3,1,2,3]
    sum_ = 0 ; count = 0 
    global goal_br,br,count_,g
    for i in range(9):
        if br[i] != goal_br[i]: # 목표 위치에 없으면 
            start = [y[i],x[i]] # 맨해튼 출발 지점
            num = br[i] # 현재 위치 숫자
            if num == 0: continue # 예 외 숫자 (0, 3??)            
            for l in [6,3,0,7,4,1,8,5,2]:
                if goal_br[l] == num: # 목표 지점을 찾으면
                    arrival = [y[l],x[l]] # 맨해튼 도착 지점
                    length.append(abs(start[0] - arrival[0]) + abs(start[1] -arrival[1]))
            sum_ += min(length)
    F.append(g + sum_)# F 값 저장 
    br_box.append(br)# 보드 저장

#astar   
def comparing_cases():
    global goal_br,br
    box = br[:] #box -> br
    for i in range(9):
        if br[i] == 0:
            for arr in [-3,3,-1,1]:
                if i in [2,5] and arr == 1: continue
                if i in [3,6] and arr == -1: continue             
                dire = i + arr
                if dire > -1 and dire < 9 and br[dire] != 0: # 0 ~ 8
                    br[i] = br[dire]
                    br[dire] = 0
                    comparing_board() # f(x)
                    br = box[:]

#astar & random
def comparing_cases_2(br,get,ice_3 = "false"):
    global goal_br
    box = br[:] #box -> br
    for i in range(9):
        if br[i] == 0:
            for arr in [-3,3,-1,1]:
                if i in [2,5] and arr == 1: continue
                if i in [3,6] and arr == -1: continue             
                dire = i + arr
                if dire > -1 and dire < 9 and br[dire] != 0: # 0 ~ 8
                    if ice_3 == "true" and br[dire] == 3: continue
                    br[i] = br[dire]
                    br[dire] = 0
                    get.append(br[:]) # 저장
                    br = box[:] #br -> box
        
def select_board():
    global br,F,br_box
    a = 0
    while True:
        a += 1
        for i in range(len(F)):
            if F[i] == a and br_box[i] not in recode:
                br = br_box[i] # 다음 노드
                recoding_board() # 노드 기록
                return -1

# 최적화
def Optimizing():
    global recode,br_box_2
    new_recode = []; save = []
    start = recode[0] # 시작 지점 저장
    recode = recode[::-1]# reverse(arrival -> start)
    li = recode[0] # 초기값
    new_recode.append(li[:]) # 초기 값 저장
    while li != start:
        comparing_cases_2(li,br_box_2)
        for i in recode[recode.index(li)+1:]:
            if i in br_box_2: save.append(i)
        li = save[-1] # 다음 비교 보드
        new_recode.append(li[:]) # 새 기록에 저장
    return new_recode[::-1]

def astar():
    global goal_br,br,g
    recoding_board() # 보드 기록
    while goal_br != br:
        g += 1
        comparing_cases() # 각 경우의 수의 f(x)
        select_board() # 노드 선택      
        del F[:], br_box[:] # reset 
    return Optimizing()
astar()
