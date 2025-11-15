from collections import deque # que

isFasten = None

def prt(board: str,num: None):
    print('',board[:3])
    print('',board[3:6],end = '   ')
    if num is not None: print("[{}]".format(num))
    print('',board[6:9])
    print('-----------')

def mr(board: str):
    board = list(board)
    board = [board[i-1] for i in [3,2,1,6,5,4,9,8,7]]
    return ''.join(board)

def change(str_br: str, now_pos: int, new_pos: int):
    br = list(str_br)
    br[now_pos],br[new_pos] = br[new_pos],br[now_pos]
    return ''.join(br)

def direction(board: str):    
    result = []
    for i in range(2): # 0 ~ 1        
        br = board[::-1] if i else board[:]
        pos = abs( (8 if i else 0) - br.index('0'))
        br = board[:]
        def rule(n,li = [-3,3,-1,1]): # 3 고정 여부
            return (br[pos+li[n]] is not '3') if isFasten else True        
        if pos not in (0,1,2) and rule(0): #up
            result.append(change(br,pos,pos - 3))
        if pos not in (6,7,8) and rule(1): #down
            result.append(change(br,pos,pos + 3))
        if pos not in (0,3,6) and rule(2): #left
            result.append(change(br,pos,pos - 1))
        if pos not in (2,5,8) and rule(3): #right
            result.append(change(br,pos,pos + 1))            
    return result

def bfs(start: str, goal: str):
    que = deque()
    que.append(start) # 첫 번째 노드 
    marked = {start: "start"} # 마킹
    board = 'str'
    while board != goal:
        board = que.popleft()
        for state in direction(board):
            if state not in marked:
                marked[state] = board
                que.append(state)
    return marked

def print_recode(start: str,goal: str,marked):
    recode = []
    node = goal
    while node != start:
        recode.append(list(map(int,node)))
        node = marked[node]
    recode.append(list(map(int,start)))
    return -1
    for i in recode[::-1]:
        prt(i,len(recode) - recode.index(i))   
 
def bfs_serch(start,goal,TorF: bool):
    global isFasten
    isFasten = TorF
    start_state = start # 시작 보드 
    goal_state = mr(goal) if isFasten else goal # 종료 보드    
    marked = bfs(start_state,goal_state)
    print_recode(start_state,goal_state,marked)   
    
bfs_serch('212012103','111222300',False)
        
