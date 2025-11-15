drl_report_line(OFF)
printf = lambda *n: tp_log(' '.join(map(str,n))) # print

set_tcp('전기그리퍼'); set_tool('tool wei')
set_velx(2500); set_accx(1800); begin_blend(25)

device = sub_program_run('device')  # 디바이스 통신 
socket = sub_program_run('socket') # 소켓 통신
write,read = device.write,device.read   # 디바이스 쓰기, 디바이스 읽기

### Part - 좌표

def posing(n:'pos',y,x):
    Len = y * x
    pos = [n] * Len 
    for i in range(1,Len):
        pos[i] = (trans(pos[i - 1],[-40,0,0,0,0,0]) if i % x else
                     trans(pos[i - x],[0,40,0,0,0,0]))
    return pos
    
pos_A = posing(posx(-259.77, 191.84, 15.19, 90,180,0),6,4)
pos_B1 = posing(posx(369.32, 321.63, 14.89, 90,180,0),4,3)
pos_B2 = posing(posx(239.05, 400.58, 15.06, 90,180,0),3,4)
pos_C = [posx(-137.38+120, 523.71, 34.32, 90,180,0),
              posx(-137.38, 523.71, 34.32, 90,180,0)]
pos_D = [posx(-79.73, 331.25, 13.1,90,180,0),
              posx(-79.73-40, 331.25, 13.1, 90,180,0)]
pos_index = posx(346.45, 254.97, 80.73, 90,180,0)
positions = [pos_A,pos_B1,pos_B2,pos_C,pos_D,pos_index]

up_value = [[0,0,35,0,0,0],[0,0,5,0,0,0]] # 상대 좌표
up = lambda pos,n=None: trans(pos,[[0,0,n[0],0,0,0],[0,0,n[1],0,0,0]][isgrip] if n != None else up_value[isgrip])
Turn = lambda pos,n: [pos[0],pos[1],pos[2],[90,135,45,0,-90,180][n],180,0]

### Part - 무빙 함수

isgrip = 0
def grip(n):
    global isgrip
    if isgrip == n: return -1
    mwait(0)
    set_tool_digital_outputs([1*n,2*-n])
    wait(0.25)
    isgrip = (0 if n == -1 else 1)
    
it_li = lambda: [read(i) for i in range(52,60)]
def it(n,t = 0.5):
    if not n: 
        return -1
    write(80 if n > 0 else 81,abs(n))
    wait((t)*abs(n))
  
def gantry(n):  
    write(82,n)
    wait(0.8)

pack = 0
def moveg(Type,pos,up_val = None,device:'통신' = True,angle=0): 
    global pack,up_value
    Pos = Turn(positions[Type][pos],angle) if Type != 5 else positions[Type]
    movel(up(Pos,up_val))
    movel(Pos)
    grip(-1 if isgrip else 1)
    if device:
        if isgrip: 
            pack = read(pos,Type)
        isexit = 20 if read(pos,Type) >= 20 else 0
        if not(isexit) and pack >= 20: pack -= 20
        write(pos,(0 if isgrip else pack)+isexit,Type)
    movel(up(Pos,up_val))

### Part - 실행 함수
                
def get_board():
    br_A = [0,None,None,None,None]
    br_B = [1,None,None,None,None]                 
    n = lambda n,Type=0: read(n,Type)    
    # board A 
    br_A[1] = ''.join(['0' if n(i) >= 20 else 'x' if n(i) == 9 else str(n(i)) for i in range(24)])
    br_A[2] = ''.join(['3' if n(i) == 2 else str(n(i)) for i in range(52,60)])
    br_A[3],br_A[4] = [i for i in range(24) if n(i) >= 20]    
    # board B 
    br_B[1] = [''.join(['1' if 10 < n(j) < 15 else 'x' if n(j) == 9 else '0' for j in range(24+i,36+i)]) for i in [0,12]]
    br_B[2] = [n(br_B[1][i].index('1'),i+1)-11 for i in range(2)]
    br_B[3] = [br_B[1][i].index('1') for i in range(2)]
    br_B[4] = [[j-(24+i) for j in range(24+i,36+i) if n(j) >= 20][0] for i in [0,12]]
    return [br_A,br_B]
    
def get_calculate_result(value):
    A_result = socket.open_server(value[0])   # A 연산 결과 
    B_result = socket.open_server(value[1]) # B 연산 결과
    return [A_result,B_result]    
    
def Run_D():
    for i in range(2):
        for j in range(4):
            n = (20 * i) + j
            if read(n) >= 10:
                moveg(0,n,[35,85])
                moveg(4,i,[35,85],False)
    
def Run_A(result):
    for i in range(len(result)):
        s,e,turn,spin_count,pack,move_dire = result[i]
        pack = 2 if pack == '12' else 1 # 토글 시켜줌 + 1: 사각, 2: 원형
        it(spin_count)  # 인덱스 회전
        if spin_count: write(51,0) # 턴 초기화
        up_value = [35,35] if pack == 2 and move_dire in [1,3,5,7] else [35,5]
        angle = (1 if move_dire in [3,7] else 2)  if pack == 1 and move_dire in [1,3,5,7] else 0
        moveg(0,s,up_value)
        if angle: 
            movel(Turn(up(pos_A[s]),angle))
            movel(Turn(up(pos_A[e]),angle))
            moveg(0,e,up_value)
        else:
            moveg(0,e,up_value)
        write(51,turn)  # 턴 표시
        
def loading_pack(pack:'1 or 2'):
    def amove_home():
        amovej([90,0]*3,200,200) # 집 경유
        wait(0.5)
    for j in range(2):
        gantry(pack)    # 겐트리 입구로
        Dire = it_li().index(pack) # 현재 인덱스 방향
        turn_ct = [(Dire+i)%8 for i in range(8)].index(4) # 정회전시 필요한 회전수
        it(-(8-turn_ct) if turn_ct > 4 else turn_ct) # 인덱스 회전
        amove_home()
        moveg(5,0,[35,85],False) # 인덱스 가서 팩 잡기
        write(56,0) # HMI
        
        amove_home()
        movel(up(pos_A[A_road[0]],[0,85]))
        for i in A_road:
            movel(up(pos_A[i],[0,5]))
        movel(up(pos_A[A_road[-1]],[0,85]))
        
        for i in range(2):
            movel(pos_C[not(i)])
            grip(1 if i else -1)
            write(pack-1,0 if i else pack,3)
            if not(i):
                 gantry(2+pack)    # 겐트리 출구로
        movel(up(pos_C[0],[0,85]))
            
        pos_B = [pos_B1,pos_B2][j]
        pos = br_B[3 if pack == 1 else 4][j]        
        movel(up(pos_B[pos],[0,100]))
        if pack == 1:
            n = read(pos,j+1) - (10)
            angle = [4,5,0,3][n - 1] # 상 우 하 좌 (팩은 아래를 바라본 모양임)
        else: angle = 0
        movel(trans(Turn(pos_B[pos],angle),[0,0,0 if pack == 1 else 60,0,0,0]))
        grip(-1)
        write(pos,n if pack == 1 else 25,j+1)
        movel(up(Turn(pos_B[pos],angle),[100,0]))
        amove_home()
            
def Run_B(result):
    for i in range(len(result)):
        B1,B2,pack_dire,move_dire = result[i]
        write(50,move_dire+1)
        for j in range(2):
            s,e = [B1,B2][j]
            if None in [s,e]:
                continue
            moveg(j+1,s)
            angle = [0,3,4,5][move_dire]
            spin_value = [0,-90,-180,90][move_dire]
            time = [0,1.2,1.5,1.2][move_dire]
            moveg(j+1,e,None,False,angle)
            val = (pack_dire[j]+1) + (20 if e == br_B[4][j] else 0)
            write(e,val,j+1)
            amovej([0,0,0,0,0,spin_value], 200, 200, mod = 1)
            wait(time)                

# M A I N

br_A,br_B = get_board() # 입력값 받기
A_result,B_result = get_calculate_result([br_A,br_B]) # 연산
A_road,A_result = A_result
printf('ready')

#B0
while not (read(98)):
    pass
write(99,1) # BUZZ

Run_D()
Run_A(A_result)
loading_pack(1)
Run_B(B_result)
loading_pack(2)

write(99,1) # BUZZ
