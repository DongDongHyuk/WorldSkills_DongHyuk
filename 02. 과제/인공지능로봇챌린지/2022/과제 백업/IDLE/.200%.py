from collections import deque
from queue import PriorityQueue
from socket import *

class State_0:      # A Soring State
    road = None     # getdire result
    def __init__(self,br,it,turn = 0,spin_count = 0,pack = '1234',move_dire = None):
        # 파레트, 인덱스 테이블(1:사각 | 3:원형), 턴수, 인덱스 돌린 횟수, 옮길 팩
        self.br,self.it,self.turn,self.spin_count,self.pack,self.move_dire = br,it,turn,spin_count,pack,move_dire

class State_1:      # A getdire State
    br,start_pos,goal_pos = [None] * 3
    Priority = {'0':1,'1':2,'2':2,'3':2,'4':2}  
    def __init__(self,pos):
        self.pos,self.pack = pos,State_1.br[pos]        # 위치, 위치에 있는 팩
    def __lt__(self,other):                             # 우선순위(빈 칸 < 팩이 있는 곳 | 작은게 우선)
        return State_1.Priority[self.pack] <  State_1.Priority[other.pack]

class State_2:      # B Soring State
    start_pos,goal_pos = [None] * 2
    def __init__(self,br,pack_dire,move_dire=None):
        self.br,self.pack_dire,self.move_dire = br,pack_dire,move_dire

def exchange(state, now, new, it=None, turn=None, spin_count=None, B1orB2=None, move_dire=None):
    def exchanging(br,now,new):
        br = list(br)
        br[now],br[new] = br[new],'0'
        return ''.join(br)
    if not G_Type:
        br = exchanging(state.br,now,new)
        pack =  (('34' if state.br[new] in '12' else '12') if state.pack == '1234' else
                 ('34' if state.pack == '12' else '12'))
        return State_0(br,it,turn + 1,spin_count,pack,move_dire)
    else: 
        new_br,new_pack_dire = [None]*2,[None]*2
        B_sqnc = [B1orB2,not(B1orB2)]
        for i in range(2):
            n = B_sqnc[i]
            size = G_size[n]
            dires_idxs = deque([0,1,2,3])
            default_dires = deque([-size[1],1,size[1],-1])              # pack_dire == 0 기준 (팩이 위를 보고 있을 때)
            dires = default_dires.copy()
            dires.rotate(state.pack_dire[n])                            # 방향 인덱스를 팩이 바라보고있는 곳을 기준으로 회전함
            dires_idxs.rotate(state.pack_dire[n])
            if not i:
                re_move_dire = dires_idxs[default_dires.index(now - new)]        # 팩이 이동한 방향 (팩이 보는 방향을 기준)
                move_dire = re_move_dire
                br = exchanging(state.br[n],now,new)
                pack_dire = default_dires.index(now - new)
            else: 
                re_move_dire = default_dires.index(default_dires[dires_idxs.index(re_move_dire)])
                new = state.br[n].index('1')        # 기본은 빈칸에서 팩을 보는 방식, 이건 팩에서 빈칸을 봄
                y,x = new // size[1], new % size[1]
                ny,nx = y + G_dy[re_move_dire],x + G_dx[re_move_dire]
                nz = ny * size[1] + nx
                # 반대 보드의 팩이 이동 가능한 방향으로 이동가능 한가
                if  0 <= ny < size[0] and 0 <= nx < size[1] and state.br[n][nz] == '0':
                    br = exchanging(state.br[n],nz,new)
                    pack_dire = default_dires.index(nz - new)
                else:
                    br,pack_dire = state.br[n],state.pack_dire[n]
            new_br[n] = br
            new_pack_dire[n] = pack_dire
        return State_2(new_br,new_pack_dire,move_dire)

def expand_sorting(state):
    result = []
    def rules(state,ny,nx,nz,size,it=None,dir_idx=None,B1orB2=None):
        br = state.br[B1orB2] if G_Type else state.br
        if  not(0 <= ny < size[0] and 0 <= nx < size[1]) or \
            br[nz] in ('x','0'):                                       # 벽 확인, 고정 팩, 중복
                return False
        if not G_Type:                                                  # Board_A
            if  br[nz] not in state.pack or \
            it[(dir_idx + 4) % 8] not in state.pack:                    # 현재 턴에 옮길 팩, 인덱스 방향 표시
                    return False
        return True

    if not G_Type:                                                      # Board_A
        n_p = [i for i in range(len(state.br)) if state.br[i] == '0']
        size = G_size
        it_states = tuple({0,state.turn,state.turn*-1})
        init_it = state.it.copy()
        for i in it_states:                                             # 모든 인덱스의 상태
            it,turn = init_it.copy(),0 if i else state.turn
            it.rotate(i)
            for pos in n_p:                                             # 모든 빈칸
                y,x = pos // size[1],pos % size[1]
                for j in range(8):                                      # 모든 방향
                    for Len in range(1,6):                              # 모든 거리(1 ~ 5)
                        ny,nx = y + (G_dy[j] * Len),x + (G_dx[j] * Len)
                        nz = ny * size[1] + nx
                        # '소' 팩
                        if Len == 1:
                            if  rules(state,ny,nx,nz,size,it,j) and \
                                state.br[nz] in '1'+'3':                # rules True 이고 '소' 팩인가
                                    result.append(exchange(state,pos,nz,it,turn,i,None,j))
                        # '중' 팩
                        ay,ax = y + -G_dy[j],x + -G_dx[j]
                        az = ay * size[1] + ax
                        if  (not(0 <= ay < size[0] and 0 <= ax < size[1]) or state.br[az] != '0') and \
                            rules(state,ny,nx,nz,size,it,j) and \
                            state.br[nz] in '2'+'4':                   # 벽이거나 팩이 있고 Rule True 이고 '중' 팩인가
                                result.append(exchange(state,pos,nz,it,turn,i,None,j))
                        else:
                            if  not(0 <= ny < size[0] and 0 <= nx < size[1]) or \
                                state.br[nz] != '0':                    # 보드 밖 이거나 팩이 있을 때
                                    break
    else:                                                               # Board_B
        for i in range(2):                                              # 모든 보드(B1,B2)
            n_p = [j for j in range(len(state.br[i])) if state.br[i][j] == '0']
            size = G_size[i]
            for pos in n_p:                                             # 모든 빈칸
                y,x = pos // size[1],pos % size[1]
                for j in range(4):
                    ny,nx = y + G_dy[j], x + G_dx[j]
                    nz = ny * size[1] + nx
                    if rules(state,ny,nx,nz,size,None,None,i):
                        result.append(exchange(state,pos,nz,None,None,None,i))
                    
    return result

def expand_getdire(stete):
    result = []
    dy,dx = (-1,0,1,0),(0,1,0,-1)       # 길찾기는 대각 안됨 
    y,x = stete.pos // G_size[1],stete.pos % G_size[1]
    for i in range(4):
        ny,nx = y + dy[i], x + dx[i]
        nz = ny * G_size[1] + nx
        if  0 <= ny < G_size[0] and 0 <= nx < G_size[1] and \
            stete.br[nz] != 'x':
                result.append(State_1(nz))
    return result

def bfs_sorting(root:'State_0 or State_2'):
    def get_br(n:'state'):
        if not G_Type:
            return n.br + str(''.join(n.it)) + str(n.turn) + str(n.pack)
        else:
            return str(n.br) + str(n.pack_dire) + str(n.move_dire)
    que = deque()
    que.append(root)
    marked = {root:'root'}
    br_marked = {get_br(root)}
    state = root
    def isleaf(br):
        if not G_Type:
            road_packs = [br[i] for i in state.road if br[i] != '0']
            return bool(road_packs)
        else:
            br = state.br      
            pack_pos = [br[0].index('1'),br[1].index('1')]  
            return pack_pos != state.goal_pos
    while isleaf(state.br):
        state = que.popleft()
        for new_state in expand_sorting(state):
            br = get_br(new_state)
            if br not in br_marked:
                marked[new_state] = state
                br_marked.add(get_br(state))
                que.append(new_state)
    marked['leaf'] = state
    return marked

def bfs_getdire(root:'State_1'):
    que = PriorityQueue()
    que.put(root)
    marked = {root.pos:'root'}
    state = root
    while state.pos != State_1.goal_pos:
        state = que.get()
        for new_state in expand_getdire(state):
            if new_state.pos not in marked:
                marked[new_state.pos] = state.pos
                que.put(new_state)
    marked['leaf'] = state.pos
    return marked

def path(marked):
    state = marked['leaf']
    path = [state]
    while marked[state] != 'root':
            state = marked[state]
            path.append(state)
    return path[::-1]

def convert(result):
    path = []
    first = result[0]
    for second in result[1:]:
        step = ([[None]*2,[None]*2,second.pack_dire,second.move_dire] if G_Type else 
                [None,None,second.turn,second.spin_count,second.pack,second.move_dire])
        for i in range(2):       
            first_br = first.br[i] if G_Type else first.br      
            second_br = second.br[i] if G_Type else second.br
            STEP = step[i] if G_Type else step
            for j in range(len(second_br)):
                if first_br[j] != second_br[j]:
                    if first_br[j] =='0': 
                        STEP[1] = j
                    else: 
                        STEP[0] = j
            if [G_Type,i] == [0,0]: 
                break
        path.append(step)
        first = second
    return path

def main(n):
    global G_Type,G_size,G_dy,G_dx
    G_Type = n[0]
    G_size = ((6,4),((4,3),(3,4)))[G_Type]
    G_dy,G_dx = [((-1,-1,0,1,1,1,0,-1),(0,1,1,1,0,-1,-1,-1)),
                 ((-1,0,1,0),(0,1,0,-1))][G_Type]

    if G_Type == 0:         # board A
        br,index_table,start,end = n[1:]
        State_1.br,State_1.goal_pos = br,end             
        getdire_result = path(bfs_getdire(State_1(start)))
        
        State_0.road = getdire_result
        sorting_result = path(bfs_sorting(State_0(br,deque(index_table))))
        result = [getdire_result,convert(sorting_result)]


    if G_Type == 1:         # board B
        br,pack_dire,start,end = n[1:]
        State_2.start_pos,State_2.goal_pos = start,end
        sorting_result = path(bfs_sorting(State_2(br,pack_dire)))
        result = convert(sorting_result)
    return result

while 1:
    Sock = socket(AF_INET, SOCK_STREAM)
    try:
        Sock.connect(('192.168.137.100',20001))
    except:
        print('.')
        continue
    else:
        try:
            n = eval(Sock.recv(1024).decode('utf-8'))
            result = main(n)
            Sock.send(bytes(str(result),'utf-8'))
        except:
            continue

