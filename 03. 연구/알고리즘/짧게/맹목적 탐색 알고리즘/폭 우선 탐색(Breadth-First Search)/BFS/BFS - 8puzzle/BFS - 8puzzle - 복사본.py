from collections import deque # que
import random

def is_solved(board: str):
    if not board: return True
    result = 0
    br = list(board)
    for i in range(9):
        count = 0
        pos = br.index(str(i))        
        for j in range(pos,9):
            if int(br[j]) < int(i): count += 1            
        result += count
    return result % 2 == 0

def random_board():
    board = []
    while 1:
        board = ['0','1','2','3','4','5','6','7','8']
        random.shuffle(board)
        if is_solved(board): break 
    board[board.index('0')] = '_'
    return ''.join(board)

def prt(board: str,num: None):
    print('',board[:3])
    print('',board[3:6],end = '   ')
    if num is not None: print("[{}]".format(num))
    print('',board[6:9])
    print('-----')

def change(str_br: str, now_pos: int, new_pos: int):
    br = list(str_br)
    br[now_pos],br[new_pos] = br[new_pos],br[now_pos]
    return ''.join(br)

def direction(br: str):
    result = []
    pos = br.index('_')
    if pos not in (0,1,2): #up
        result.append(change(br,pos,pos - 3))
    if pos not in (6,7,8): #down
        result.append(change(br,pos,pos + 3))
    if pos not in (0,3,6): #left
        result.append(change(br,pos,pos - 1))
    if pos not in (2,5,8): #right
        result.append(change(br,pos,pos + 1))
    return result

def bfs(start: str, goal: str):
    que = deque()
    que.append(start) # 첫 번째 노드 
    marked = [(start,"start")]
    board = 'str'
    while board != goal:
        if len(marked) > 50000: print(len(marked))
        board = que.popleft()
        for state in direction(board):
            if state not in marked:
                marked.append((state,board))#(자식 노드,부모 노드)
                que.append(state)
    return marked

def print_recode(start: str,goal: str,marked):
    recode = []
    node = goal
    while node != start:
        recode.append(node)
        for i in range(len(marked)): # 현재 노드를 찾음 
            if marked[i][0] == node:
                pos = i; break
        node = marked[pos][1] # 현재 노드의 부모노드를 저장
    recode.append(start)
    for i in recode[::-1]:
        prt(i,len(recode) - recode.index(i))
    
def main():
    #start_state = random_board()
    start_state = '16784352_'
    goal_state = '_12345678'

    marked = bfs(start_state,goal_state)
    #print(marked)
    #print_recode(start_state,goal_state,marked)
    
    print("start: {}".format(start_state))
    print("visited_node: {}".format(len(marked)))    
 
   
main()
