from copy import deepcopy

# 1차원 배열 이쁘게 프린트
def printl(a,string = "none",count = 1):
    for i in range(9): print(a[i], " ") if count % 3 == 0 else print(a[i], end = ' '); count += 1
    if string == "": print("")
    
goal_br = [2,2,1,
           1,1,2,
           0,0,3]
br= [2,1,2,
     1,1,2,
     3,0,0]

num_br = num_goal_br = [0] * 9

#맨해튼 거리 계산
def Mht(start_y,start_x,arrival_y,arrival_x):
    return abs(start_y - arrival_y) + abs(start_x - arrival_x)

#거울 모드 변환
def mr(b, count = 0, result = [0] * 9): # convert mirror
    for i in [3,2,1,6,5,4,9,8,7]:
        result[count] = b[i-1]
        count+=1
    return result

#숫자 매기기
def put_num(a,b,count = 1):
    box = [deepcopy(a),deepcopy(b)]
    for i in range(9): #br
        num = b[i]
        if num == 0: continue
        for l in range(9):
            if a[l] == num:
                a[l] = -1
                num_br[l] = i+1
                break
    for i in range(9): #goal_br
        if a[i] != 0:
            num_goal_br[i] = count
            count+=1
    a = deepcopy(box[0])
    b = deepcopy(box[1])
    
    
#보드 비교
def cm_br(a,b,count = 0):
    print("goal_board"); printl(a)
    print("board_cases"); printl(b)
    for y in range(1,4):
        for x in range(1,4):
            turn = ((y-1)*3+x)-1
            if a[turn] != b[turn]: # if not goal pos
                print(y,x)            
                
#경우의수 비교              
def cm_cases(a,b):
    copy_br = deepcopy(b)# 최초 보드 저장 
    for i in range(9):
        if b[i] == 0:
            for d in [-3,3,-1,1]:
                if i in [2,5] and d == 1: break
                if i in [3,6] and d == -1: break                
                dire = i + d
                if dire > -1 and dire < 9 and b[dire] != 0: # 0 ~ 8
                    box = b[dire] # br[dire] -> box
                    b[dire] =b[i] # br[i] -> br[dire]                     
                    b[i] = box # box -> br[i]
                    cm_br(a,b)# 목표 배치가 아닌 숫자의 h의 합
                    b = deepcopy(copy_br)# 최초 보드 불러오기

# goal_br = a / br = b 
put_num(goal_br,br) # 숫자 매기기(br,goal_br)

cm_br(num_goal_br,num_br)


    
    
