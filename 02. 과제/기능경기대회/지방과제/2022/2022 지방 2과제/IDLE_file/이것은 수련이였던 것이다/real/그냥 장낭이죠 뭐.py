import random as r

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
br= [2,0,0,  
     2,1,1, 
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

mix_br = r.shuffle(br)
printl(list(mix_br))

