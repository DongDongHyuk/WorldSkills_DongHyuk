from copy import deepcopy

F = []; br_box = []; recode_br = []
g = 1 # int

# 2차원 배열 이쁘게 프린트
printl_2 = lambda list_: list(map(lambda a : print(a),list_))

# 1차원 배열 이쁘게 프린트
def printl(a,string = "none",count = 1):
    for i in range(9):
        print(a[i], " ") if count % 3 == 0 else print(a[i], end = ' ')
        count += 1
    if string == "": print("")
    
goal_br = [1,1,1,
           2,2,2,
           3,0,0]
br= [0,2,3,
     1,2,1,
     1,2,0]

#기록
def recoding_node():
    global br,recode_br
    re_id = br[:]
    recode_br.append(re_id) # 노드를 저장함
    
#sum_Manhattan_distance
def comparing_board(): 
    start = [0] * 2; arrival = [0] * 2; length = [];
    posy = [1,1,1,2,2,2,3,3,3]; posx = [1,2,3,1,2,3,1,2,3]
    sum_ = 0 ; count = 0 
    global goal_br,br
    for i in range(9):
        if br[i] != goal_br[i]: # 목표 위치에 없으면
            start = [posy[i],posx[i]] # 맨해튼 출발 지점
            for l in range(9):
                if goal_br[l] ==br[i]: # 목표 지점을 찾으면
                    arrival = [posy[l],posx[l]] # 맨해튼 도착 지점
                    sum_ += abs(start[0] - arrival[0]) + abs(start[1] -arrival[1])
    F.append(sum_)# F 값 저장 
    br_box.append(br)# 보드 저장
    
# 현재 보드의 경우의 수
def comparing_cases():
    global goal_br,br,g
    g += 1 # cost
    box = deepcopy(br) #box -> br
    for i in range(9):
        if br[i] == 0:
            for arr in [-3,3,-1,1]:
                if i in [2,5] and arr == 1: continue
                if i in [3,6] and arr == -1: continue             
                dire = i + arr
                if dire > -1 and dire < 9 and br[dire] != 0: # 0 ~ 8
                    box_0 = br[dire] # box_0 -> br[dire]
                    br[dire] = br[i] # br[dire] -> br[i]
                    br[i] = box_0 # br[i] -> box_0(br[dire])
                    printl(br,"")
                    comparing_board() # f(x)
                    br = deepcopy(box) #br -> box

#selecting_node            
def comparing_node():
    global br,F,br_box
    print(F); print("")
    break_ = min_ = 0
    while break_ == 0:
        min_+=1
        for i in range(len(F)):
            if F[i] == min_:
                if br_box[i] not in recode_br:
                    br = br_box[i] # 다음 노드
                    printl(br,"")
                    break_ = 1

def astar():
    global goal_br,br,F,br_box
    print("goal_br_state"); printl(goal_br,"")
    print("br_state"); printl(br,"")
    #while goal_br != br:
    recoding_node() # 노드 기록
    comparing_cases() # 각 경우의 수의 f(x)
    comparing_node() # 노드 선택        
    print("complete !!!"); print("")
astar()


