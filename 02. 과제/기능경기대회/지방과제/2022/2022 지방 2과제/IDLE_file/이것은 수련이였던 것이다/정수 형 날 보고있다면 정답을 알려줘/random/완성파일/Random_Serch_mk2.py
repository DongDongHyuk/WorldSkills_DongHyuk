import time 

br_box = []; br_box_2 = []; recode = []
state = "same"
    
goal_br = [1,2,1,
           2,1,2,
           3,0,0]
br= [1,2,1,
     2,2,1,
     0,0,3]

# convert mirror
def mr(board):
    count = 0; result = [0] * 9
    for i in [3,2,1,6,5,4,9,8,7]:
        result[count] = board[i-1]
        count+=1
    return result

#기록
def recoding_board():
    global br,recode
    re_id = br[:] # id가 겹쳐서 re_id를 겹침
    recode.append(re_id) # 노드를 저장함

# 현재 보드의 경우의 수    
def comparing_cases(br,get = br_box):
    global goal_br
    box = br[:] #box -> br
    for i in range(9):
        if br[i] == 0:
            for arr in [-3,3,-1,1]:
                if i in [2,5] and arr == 1: continue
                if i in [3,6] and arr == -1: continue             
                dire = i + arr
                if dire > -1 and dire < 9 and br[dire] != 0:
                    a = br[dire] # a -> br[dire]
                    br[dire] = br[i] # br[dire] -> br[i]
                    br[i] = a # br[i] -> a(br[dire])
                    get.append(br[:]) # 저장
                    br = box[:] #br -> box
                    
# 보드 선택
def select_board():
    global goal_br,br,br_box, recode
    for i in br_box:
        if i not in recode:
            br = i # 다음 보드
            recoding_board() # 보드 저장
            break
        else: continue

# 최적화
def Optimizing():
    global recode,br_box_2
    new_recode = []; save = []    
    start = recode[0] # 시작 지점 저장
    recode = recode[::-1]# reverse(arrival -> start)
    li = recode[0] # 초기값
    new_recode.append(li[:]) # 초기 값 저장
    while li != start:
        comparing_cases(li,br_box_2)
        for i in recode[recode.index(li)+1:]:
            if i in br_box_2: save.append(i)
        li = save[len(save)-1] # 다음 비교 보드
        new_recode.append(li[:]) # 새 기록에 저장
    print("complete !!! step: {}".format(len(new_recode)))
        
def ramdom_serch():
    global goal_br,br,state,br_box
    goal_br = mr(goal_br)
    recoding_board() # 저장
    if goal_br.index(3) != br.index(3):
        goal_br = [1,1,1,2,2,2,0,3,0]
        state = "diff"
    start = time.time()
    while goal_br != br:
        if state == "diff" and goal_br.index(3) == br.index(3): # 한번만 실행
            br_box.clear(); state = "same"
        comparing_cases(br, br_box) # 지금 보드에서 한 칸 움직여 가능한 보드를 보여줌
        select_board() # 보드 선택
    Optimizing() # 최적화
    end = time.time()
    print("Idle {} 초 걸렸습니다.".format(round(end - start,4)))
    print("Dart {} 초 걸렸습니다.".format(round(end - start,4)*100))
    
ramdom_serch()

