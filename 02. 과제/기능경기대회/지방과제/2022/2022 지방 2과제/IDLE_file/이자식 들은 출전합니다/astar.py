br_list = br_list2 = []
recode = []; F = [] # list
G = 1 # int
    
goal_br = [1,1,1,
           2,2,2,
           3,0,0]
br= [2,2,0,
     1,1,0,
     1,2,3]

recoding = lambda li: recode.append(li[:])
    
def MHT():
    mht  = []; result = 0
    y = [1,1,1,2,2,2,3,3,3]; x = [1,2,3,1,2,3,1,2,3]
    for i in range(9):
        if br[i] != goal_br[i] and br[i] != 0:
            start = [y[i],x[i]]
            for j in range(9):
                if goal_br[j] == br[i]:
                    arrival = [y[j],x[j]]
                    mht.append(abs(start[0] - arrival[0])+abs(start[1] - arrival[1]))
            result += min(mht)
    F.append(G + result); br_list.append(br)

def cases(board, serch, fix3, get):
    if board == "global": global br
    else: br = board[:]
    save = br[:]
    for i in range(9):
        if br[i] == 0:
            for j in [-3,3,-1,1]:
                dire = i + j
                if i in [2,5] and j == 1: continue
                if i in [3,6] and j == -1: continue
                if -1 < dire < 9 and br[dire] != 0:
                    br[i] = br[dire]
                    br[dire] = 0
                    if serch == "astar": MHT()
                    else: get.append(br)
                    br = save[:]
        
def select_astar(count = 0):
    global br
    while True:
        count += 1
        for i in range(len(F)):
            if F[i] == count and br_list[i] not in recode:
                br = br_list[i]
                recoding(br)
                return -1

def Optimizing():
    global recode
    new_recode = []; result = []
    recode = recode[::-1]
    br = recode[0]
    new_recode.append(br[:])
    while br != recode[-1]:
        cases(br,"optimizing","false",br_list2)
        for i in recode[recode.index(br):]:
            if i in br_list2: result.append(i)
        br = result[-1]
        new_recode.append(br)
    print("complete !!! step: {}".format(len(new_recode)))
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

def astar():
    global goal_br,br,G
    recoding(br) # 보드 기록
    while goal_br != br:
        G += 1
        cases("global","astar","false",[])# fixed
        select_astar() # 노드 선택
        del F[:], br_list[:] # reset
    return Optimizing()

result = converter(astar())
print(result)
