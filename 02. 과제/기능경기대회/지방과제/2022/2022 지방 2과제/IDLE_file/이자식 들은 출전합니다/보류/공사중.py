F = []; br_box = []; recode_br = []# list
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
           0,0,3]
br= [0,2,3,
     1,2,1,
     1,2,0]

#기록
def recoding_node():
    global br,recode_br
    re_id = br[:] # id가 겹쳐서 re_id를 겹침
    recode_br.append(re_id) # 노드를 저장함
    
# 현재 보드의 경우의 수
def comparing_cases(role = 0):
    global goal_br,br
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
                    comparing_board(role) # f(x)
                    br = deepcopy(box) #br -> box
         
def selecting_node():
    global br,F,br_box
    for i in range(len(F)):
        if F[i] == min(F):
            if br_box[i] not in recode_br:
                br = br_box[i] # 다음 노드
                break
            
def astar():
    global goal_br,br
    goal_br = mr(goal_br) 
    print("goal_br_state"); printl(goal_br,"")
    print("br_state"); printl(br,"")
    while goal_br != br:
        recoding_node() # 노드 기록
        comparing_cases() # 각 경우의 수의 f(x)
        comparing_node() # 노드 선택  
        F.clear(); br_box.clear() # reset
        
    if goal_br == br: # 완성 하셨나요?
        print("complete !!! "); print("")

astar()


