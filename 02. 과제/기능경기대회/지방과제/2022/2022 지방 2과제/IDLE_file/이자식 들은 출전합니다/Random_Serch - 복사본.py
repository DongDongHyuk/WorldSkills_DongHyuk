br_box = []; br_box_2 = []; recode = []
    
goal_br = [0,2,2,
           0,1,1,
           3,2,1]
br= [1,2,1,
     1,2,2,
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

def comparing_cases(br,get,fix_3,serch):
    global goal_br
    save = br[:] #box -> br
    for i in range(9):
        if br[i] == 0:
            for arr in [-3,3,-1,1]:
                if i in [2,5] and arr == 1: continue
                if i in [3,6] and arr == -1: continue             
                dire = i + arr
                if dire > -1 and dire < 9 and br[dire] != 0: # 0 ~ 8
                    if fix_3 == "true" and br[dire] == 3: continue
                    br[i] = br[dire]
                    br[dire] = 0
                    if serch == "astar": comparing_board() # f(x)
                    if serch == "random": get.append(br[:]) # 저장
                    br = save[:] #br -> box
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
        comparing_cases(li,br_box_2,"true","random")
        for i in recode[recode.index(li)+1:]:
            if i in br_box_2: save.append(i)
        li = save[len(save)-1] # 다음 비교 보드
        new_recode.append(li[:]) # 새 기록에 저장
    print("complete !!! step: {}".format(len(new_recode)-1))
    return new_recode[::-1]
        
def ramdom_serch():
    global goal_br,br
    goal_br = mr(goal_br)
    recoding_board() # 저장
    while goal_br != br:
        comparing_cases(br, br_box,"true","random")
        select_board() # 보드 선택
    return Optimizing() # 최적화
    
A = ramdom_serch()

def converter(li):
    new_li = []
    for i in range(len(li)):
        for l in range(9):
            if li[i][l] == 0 and li[i+1][l] != 0: a = l
            if li[i+1][l] == 0 and li[i][l] != 0: b = l
        new_li.append(b)
        new_li.append(a)
        if li[i+1] == li[len(li)-1]:
            return new_li

li_1 = []       
converter(A)
print(converter(A))
print(br)
                
        

