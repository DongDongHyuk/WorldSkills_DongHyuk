import time as t
drl_report_line(OFF)
printf = lambda n: tp_log("{}".format(n)) # tp_log !!!

w = '5 0 0 W S S 0 1 0 6 % D W 0 0 0 0 0 0 0 4'.split()
r = '5 0 0 R S S 0 1 0 6 % D W 0 0 0 4'.split()
w[0],r[0] = [5] * 2
w[-1],r[-1] = [4] * 2

for i in [w,r]:
    i[1:-1] = list(map(lambda a: ord(a),i[1:-1]))

def write(ad , val):
    ser = serial_open(port = 'COM')
    w[13] = ord(str(ad // 100))
    w[14] = ord(str((ad%100)//10))
    w[15] = ord(str(ad%10))
    w[18] = ord(str(0)) if val < 16 else ord(hex(val)[2])
    w[19] = ord(hex(val)[2]) if val < 16 else ord(hex(val)[3])
    ser.write(bytearray(w))
    serial_close(ser)
    wait(0.02)

def read(ad):
    ser = serial_open(port = 'COM')
    r[13] = ord(str(ad // 100))
    r[14] = ord(str((ad%100)//10))
    r[15] = ord(str(ad%10))
    ser.write(bytearray(r))
    wait(0.02)
    n = int(ser.read(ser.inWaiting()).decode()[10:14],16)
    serial_close(ser)
    return n 
    
set_velx(1000); set_accx(1000)

A = [posx(328.78, 321.93, 185, 90, 180, 0)] * 10
B = [posx(58.03, 380.68, 185, 90, 180, 0)] * 6
C = [posx(-171.48, 280.22, 185, 90, 180, 0)] * 24

for_li = [0,1,6,7,2,3,8,9,4,5]
for i in for_li:
    count = for_li.index(i)
    if count == 0:continue
    if count % 4 == 0: A[i] = trans(A[for_li[count - 4]],[0,40,0,0,0,0])
    else: A[i] = trans(A[for_li[count - 1]],[-40,0,0,0,0,0])

for i in range(1,6):
    if i % 4 != 0: B[i] = trans(B[i - 1],[-40,0,0,0,0,0])
    else: B[i] = trans(B[1],[0,40,0,0,0,0])

for i in range(1,24):
    if i == 12: C[i] = trans(C[2],[-40,0,0,0,0,0])
    else:
        if i % 3 == 0: C[i] = trans(C[i - 3],[0,40,0,0,0,0])
        else: C[i] = trans(C[i - 1],[-40,0,0,0,0,0])
  
up_pos = [[0,0,5,0,0,0],[0,0,38,0,0,0],[0,0,65,0,0,0]]# 업 포스
way_point = posx(-6.15, 453.53, 275.82, 116.59, -179.99, 106.59) # A 에서 C 이동시 경유지
    
A_1 = [0] * 4
A_2 = [read(i) for i in range(29,35)]
B_1 = [1,0,0,0]
B_2 = 1
C_1 = [read(i) for i in range(1,10)]
C_3 = [read(i) for i in range(13,22)]
C_2 = [0] * 3
C_4 = [0] * 3

def read_board(board):
    for i in [1,1,2,2]: board[board.index(0)] = i    

goal_br = C_1[:]
br = C_3[:]
read_board(br)
serch_result = [0] * 3
br_list = []; br_list2 = []; recode = []
G = 1; F = []

mr = lambda li: [li[i-1] for i in [3,2,1,6,5,4,9,8,7]]
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
                    mht.append(abs(start[0]-arrival[0])+abs(start[1]-arrival[1]))
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
                    if fix3 == "true" and br[dire] == 3: continue
                    br[i] = br[dire]
                    br[dire] = 0
                    if serch == "astar": MHT()
                    else: get.append(br)
                    br = save[:]                  
def reset():
    del br_list[:], br_list2[:],recode[:],F[:]
    G = 1
    
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
    printf("complete !!! step: {}".format(len(new_recode)))
    return new_recode[::-1]
    
def select_astar(count = 0):
    global br
    while True:
        count += 1
        for i in range(len(F)):
            if F[i] == count and br_list[i] not in recode:
                br = br_list[i]
                recoding(br)
                return -1

def select_random():
    global br
    for i in br_list:
        if i not in recode:
            br = i
            recoding(br)
            return -1
            
def converter(li):
    new_li = []
    for i in range(len(li)):
        for l in range(9):
            if li[i][l] == 0 and li[i+1][l] != 0: a = l
            if li[i+1][l] == 0 and li[i][l] != 0: b = l
        new_li.append(b)
        new_li.append(a)
        if li[i+1] == li[len(li)-1]: 
            reset() # 사용 했던 모든 변수 초기화
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

def random_serch():
    global goal_br,br
    goal_br = mr(goal_br)# 거울 모드
    recoding(br) # 저장
    while goal_br != br:
        cases("global","random","true",br_list)
        select_random() # 보드 선택
        return Optimizing() # 최적화

#=========================================
    
# buzz !!!
buzz = lambda a: -1 #write(100,a)

# 그리퍼
def grip(a):
    wait(0.1)
    set_tool_digital_outputs([1*a,2*-a])
    wait(0.1)
    
# z 축이 n보다 낮으면 n 까지 올리기
def up(n):    
    now_pos = get_desired_posx()
    if now_pos[2] < n: movel([0,0,n - now_pos[2],0,0,0],mod = 1)
    
#1: close / 0: open
def open_close(n):
    global B_2
    if B_2 == n: return -1
    begin_blend(2)
    B_2 = n
    a = 5 if n == 0 else 4
    movel(trans(B[a],up_pos[1]))
    movel(B[a])
    grip(1)
    write(int(1560/(39+n)),0) # 39 open / 40 close
    movec(trans(B[int(20/a)],[0,0,2,0,0,0]),B[int(20/a)],1800,1800)
    grip(-1)
    buzz(2)
    write(39+n,3)
    movel(trans(B[int(20/a)],up_pos[1]))

def up_down(next_floor):
    begin_blend(2)
    now_floor = B_1.index(1)
    if now_floor == next_floor-1: return -1
    open_close(1)
    B_1[now_floor] = 0
    movel(trans(B[now_floor],up_pos[1]))
    movel(B[now_floor])
    grip(1)
    write(35+now_floor,0)
    movec(trans(B[next_floor-1],[0,0,1,0,0,0]),B[next_floor-1],1800,1800)
    grip(-1)    
    write(34+next_floor,3)
    B_1[next_floor-1] = 1
    movel(trans(B[next_floor-1],up_pos[1]))
    open_close(0)
    
    
# 팩 놓기 
def put_pack():
    begin_blend(10)
    global A_1,C_4
    for i in range(2):
        now_pack = A_1[1-i]
        if i == 0:movel(trans(A[7-i],up_pos[1]))
        else: movec(way_point,trans(A[7-i],up_pos[1]))
        movel(A[7-i])
        grip(1)
        write(26-i,0)
        A_1[1-i] = 0
        movel(trans(A[7-i],up_pos[2]))
        if now_pack != 3: 
            movec(way_point,trans(C[12+C_3.index(0)],up_pos[2])) #왼쪽 위부터 팩이 없는곳
            movel(C[12+C_3.index(0)]) # 밑으로
            grip(-1)
            write(13+C_3.index(0),now_pack) # HMI
            C_3[0+C_3.index(0)] = now_pack
        else:   # 3 팩일때 
            movec(way_point,trans(C[21+C_4.index(0)],up_pos[2]))
            movel(C[21+C_4.index(0)])
            grip(-1)
            write(22+C_4.index(0),now_pack)
            C_4[C_4.index(0)] = now_pack
        movel(up_pos[1], mod = 1)    
    
#팩 싣기, 옮기기 
def load_pack(): 
    begin_blend(10)
    global A_2,C_2
    next_floor = [0] * 6
    int_list = [3,1,3,1,2,2]
    A_2_copy = A_2[:]
    for i in range(6):
        a =  A_2_copy.index(int_list[i])
        A_2_copy[a] = 0
        next_floor[i] = 4 if a in [0,1] else 3 if a in [2,3] else 2
    for i in [0,2,4]: # next_floor = 4,2,4,2,3,3
        for l in range(2):
            up_down(next_floor[i+l]) #[0,1/2,3/4,5]  
            index_pos = A_2.index(int_list[i+l])
            movel(trans(A[index_pos],up_pos[1]))
            movel(A[index_pos])
            grip(1)
            write(29+index_pos,0) # HMI
            A_2[index_pos] = 0
            my_seat = 6+A_1.index(0) # 7 ~ 10 승강기 빈 자리
            movec(trans(A[my_seat],[0,0,40,0,0,0]),A[my_seat],1200,1200)            
            grip(-1)
            write(my_seat+19,int_list[i+l])
            A_1[A_1.index(0)] = int_list[i+l]
            movel(trans(A[my_seat],up_pos[1]))
        up_down(1) # 1층으로
        put_pack() # 0 ~ 1
    for i in [[35,36,37,38],[39,40]]:
        for l in range(len(i)):
            if read(i[l]) == 3:
                movel(trans(B[i[l]-35],up_pos[1]))
                movel(B[i[l]-35])
                grip(1)
                write(i[l],0)
                movel(trans(B[i[l]-35],up_pos[2]))  
                movel(trans(C[9+C_2.index(0)],up_pos[2]))
                movel(C[9+C_2.index(0)])
                grip(-1)
                write(10+C_2.index(0),3)
                C_2[C_2.index(0)] = 3
                movel(up_pos[1],mod = 1)
                break    
                
def serch():
    start = t.time()
    global serch_result,br,goal_br
    serch_result[0] = converter(random_serch()) # C - 3 거울 배치
    
    goal_br = [1,1,1,2,2,2,3,0,0]
    serch_result[1] = converter(astar()) # C - 3 재배치
    
    br = C_1[:]
    serch_result[2] = converter(astar()) # C - 1 재배치    
    tp_log("ready !!! {} sec".format(round(t.time() - start,2)))
                
def solving_puzzle():
    begin_blend(2)
    global serch_result,C_1,C_3
    count = maintain = 0
    # 거울 배치, C - 3 재배치, C - 1 재배치
    err = [12,0,12] # 오차
    for li in serch_result: # 거울 배치. 재 배치
        for j in range(0,len(li),2):
            now = err[count]+li[j] # 옮길 팩 위치 = 오차 + 현재 위치 
            next = err[count]+li[j+1]  # 옮길 위치 = 오차 + 다음 위치
            if maintain == 0: # 유지
                movel(trans(C[now],up_pos[1])) # 현재 위치 위에가서  
                movel(C[now]) # 내려가 
                grip(1) # 잡아 
                num = read(now+1) # 잡은 팩 값을 받아 
            else: 
                maintain = 0
            write(now+1,0) # 그리고 원래 자리에 값 지워
            movec(trans(C[next],[0,0,1,0,0,0]),C[next],2000,2000) # 깡총 
            if len(li) > j+2 and li[j+1] == li[j+2]: 
                maintain = 1
                continue 
            grip(-1) # 뱉어 
            write(next+1,num) # 아까 저장한 겂을 적어
            movel(trans(C[next],up_pos[1])) # 위로 올라와
        count += 1 # 오차를 바꿔줄 카운트
        if li == li_1:
            buzz(2)
            wait(0.31)
            buzz(2)
    for i in [[9,7],[10,8],[21,19],[22,20]]: # 마지막 3팩 이동
        movel(trans(C[i[0]],up_pos[1]))
        movel(C[i[0]])
        grip(1)
        write(i[0]+1, 0)
        if i in [[9,7],[10,8]]:
            movec(trans(C[i[1]],[0,0,1,0,0,0]),C[i[1]])
        else:
            movel(trans(C[i[0]],up_pos[2]))
            movel(trans(C[i[1]],up_pos[2]))
            movel(C[i[1]])
        grip(-1)
        write(i[1]+1,3)
        movel(trans(C[i[1]],up_pos[1]))
    buzz(3) # 완성 부저
            
def test():
    grip(-1) # grip off
    up(300)
    #movel(trans(B[0],up_pos[1]))
    serch() # 보드 계산
    exit()
    begin_blend(5)
    while True:
        if get_digital_input(1) == 0: continue
        start = time.time()  # 시작 시간 저장
        buzz(1)# 0.5
        load_pack() # 팩 옮기기
        solving_puzzle() # 정렬
        tp_log("all complete !!! {}sec".format(round(time.time() - start,4)))
        return 1        
# ***
test()
