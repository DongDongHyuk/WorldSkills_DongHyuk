from collections import deque # que

def prt(board: str, text = None): # board_ex: '12,1,8,0,6,13,0,2,11,4,3,10,7,9,5,-1'
    isSmall = lambda n:"EX" if n == '-1' else ' '+n if (int(n) < 10) else  n
    board = ' '.join(map(isSmall,board.split(',')))
    print('',board[:12],end = '  ') # 4
    print("[{}]".format(text))
    print('',board[12:24]) # 4 8
    print('',board[24:36]) # 8 12
    print('',board[36:48]) # 12 16
    print('-------------')

def change(br: str, now_pos: int, next_pos: int):
    br = br.split(',')
    br[now_pos],br[next_pos] = br[next_pos],br[now_pos]
    return ','.join(br)

def Truedirections(br: str):
    br = br.split(',') # str -> list
    num_pos = []
    for i in range(len(br)):
        if not int(br[i]): num_pos.append(i)
    br = ','.join(br) # list -> str
    result = []
    rule = lambda n: bool(n not in ['-1','0']) # 출구,공백
    for pos in num_pos: # pos: int
        if pos not in list(range(4)) and rule(pos-4):
            result.append(change(br,pos,pos-4))
        if pos not in list(range(12,16)) and rule(pos+4):
            result.append(change(br,pos,pos+4))
        if pos not in list(range(0,13,4)) and rule(pos-1):
            result.append(change(br,pos,pos-1))
        if pos not in list(range(3,17,4)) and rule(pos+1):
            result.append(change(br,pos,pos+1))
    return result 

def isDone(br: str, num: int):
    br = br.split(',')
    num_pos = br.index(str(num))
    return (num_pos not in [11,14])   

def BFS(br: str, target: int):
    marked = {br:'start'}
    que = deque()
    que.append(br)
    node = que[0]
    while isDone(node,target):
        node = que.popleft()
        for connect_nodes in Truedirections(node):
            if connect_nodes not in marked:
                marked[connect_nodes] = node
                que.append(connect_nodes)
    marked['arrival'] = node
    return marked

def recoding(marked: dict):
    start = ''.join([i for i, j in marked.items() if j == 'start'])
    arrival = ''.join([j for i, j in marked.items() if i == 'arrival'])
    node = arrival
    recode = []
    while node != start:
        recode.append(node)
        node = marked[node]
    return recode[::-1]

def main(board: str, target: int):
    print("     [{}]".format(target))
    prt(board,'start')
    marked = BFS(board,target)
    recode = recoding(marked)
    for count,i in enumerate(recode):
        prt(i,count+1)
    return recode[-1]

main('12,1,8,0,6,13,0,2,11,4,3,10,7,9,5,-1',1)
