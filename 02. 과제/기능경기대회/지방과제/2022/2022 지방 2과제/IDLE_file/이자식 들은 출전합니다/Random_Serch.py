def printl(a,string = "none",count = 1):
    for i in range(9):
        print(a[i], " ") if count % 3 == 0 else print(a[i], end = ' ')
        count += 1
    if string == "": print("")

br_box = []; br_box_2 = []; recode = []

goal_br = [1,2,2,
           0,1,0,
           3,2,1]
br= [2,1,2,
     0,1,2,
     1,0,3]

# convert mirror
mr = lambda li: [ li[i-1] for i in [3,2,1,6,5,4,9,8,7]]

recoding = lambda li: recode.append(li[:]) 

def comparing_cases(fix_3,serch,board,get):
    global goal_br
    if board == "global": global br
    else: br = board[:]
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
                    if serch in ["random","optimizing"]: get.append(br[:]) # 저장
                    br = save[:] #br -> boxe

def select_board_random_serch():
    global br
    for i in br_box:
        if i not in recode:
            br = i # 다음 보드
            recoding(br) # 보드 저장
            return -1

def Optimizing():
    global recode,br_box_2
    new_recode = []; save = []
    start = recode[0] # 시작 지점 저장
    recode = recode[::-1]# reverse(arrival -> start)
    li = recode[0] # 초기값
    new_recode.append(li[:]) # 초기 값 저장
    while li != start:
        comparing_cases("false","optimizing",li,br_box_2)
        for i in recode[recode.index(li)+1:]:
            if i in br_box_2: save.append(i)
        li = save[-1] # 다음 비교 보드
        new_recode.append(li[:]) # 새 기록에 저장
    print("complete !!! step: {}".format(len(new_recode)-1))
    return new_recode[::-1]

def converter(li):
    new_li = []
    for i in range(len(li)):
        for l in range(9):
            if li[i][l] == 0 and li[i+1][l] != 0: a = l
            if li[i+1][l] == 0 and li[i][l] != 0: b = l
        new_li.append(b); new_li.append(a)
        if li[i+1] == li[-1]:
            return new_li
        
def random_serch():
    global goal_br,br
    goal_br = mr(goal_br)# 거울 모드
    recoding(br) # 저장
    while goal_br != br:
        comparing_cases("true","random","global",br_box)
        select_board_random_serch() # 보드 선택
    return Optimizing() # 최적화

print(random_serch())




