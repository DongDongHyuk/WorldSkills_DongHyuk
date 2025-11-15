from copy import deepcopy

br_box = []; node_box = []; recode_br = [] # list

# 2차원 배열 이쁘게 프린트
printl_2 = lambda list_: list(map(lambda a : print(a),list_))

# 1차원 배열 이쁘게 프린트
def printl(a,string = "none",count = 1):
    for i in range(9):
        print(a[i], " ") if count % 3 == 0 else print(a[i], end = ' ')
        count += 1
    if string == "": print("")
    
goal_br = [1,2,0,
           1,2,0,
           1,2,3]
br= [1,1,0,
     2,2,0,
     3,2,1]

# convert mirror
def mr(board, count = 0, result = [0] * 9):
    for i in [3,2,1,6,5,4,9,8,7]:
        result[count] = board[i-1]
        count+=1
    return result

# 노드 저장
def recoding_node():
    global br,recode_br
    re_id = br[:] # id가 겹쳐서 re_id를 겹침
    recode_br.append(re_id) # 노드를 저장함

#selecting_node            
def comparing_node():
    global br,br_box
    for i in range(len(br_box)):
        if br_box[i] in recode_br: continue
        else: pass
        br = br_box[i] # 다음 노드
        break

# 현재 보드의 경우의 수    
def comparing_cases():
    global goal_br,br
    box = deepcopy(br) #box -> br
    for i in range(9):
        if br[i] == 0:
            for arr in [-3,3,-1,1]:
                if i in [2,5] and arr == 1: continue
                if i in [3,6] and arr == -1: continue             
                dire = i + arr
                if dire > -1 and dire < 9 and br[dire] != 0 and br[dire] != 3: # 0 ~ 8
                    box_0 = br[dire] # box_0 -> br[dire]
                    br[dire] = br[i] # br[dire] -> br[i]
                    br[i] = box_0 # br[i] -> box_0(br[dire])
                    br_box.append(br)
                    br = deepcopy(box) #br -> box

# 리스트 비교
def comparing_li(li,li2,count = 0):
    for i in range(len(li)):
        if li[i] != li2[i]:
            count += 1
    return count

def optimizating(print_ = "off",count = 0, li_box = []):
    global recode_br
    print("optimizating,,,"); print("")
    li = (recode_br[len(recode_br)-1])
    for i in recode_br[::-1]:
        dif_num = comparing_li(li,i)
        if dif_num == 2:
            li_box.append(i)
            count += 1
            li = i[:]
    print("complete !!! step: {}".format(count));print("")
    if print_ == "on": [printl(i,"") for i in li_box[::-1]]
            
def random(count = 0):
    global goal_br,br,F,g,count_,br_box,recode_br
    goal_br = mr(goal_br) 
    print("goal_br_state"); printl(goal_br,"")
    print("br_state"); printl(br,"")
    print("calculating,,,"); print("")
    recoding_node() #최초 노드 기록
    while goal_br != br:
        comparing_cases()
        comparing_node()
        recoding_node()
        #printl(br,"")
        count += 1
    if goal_br == br: # 완성 하셨나요?
        print("complete !!! step: {}".format(count)); print("")
        optimizating("on")    
        

random()


