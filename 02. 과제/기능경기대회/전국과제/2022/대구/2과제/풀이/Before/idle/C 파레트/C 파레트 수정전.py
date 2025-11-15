from collections import deque # que

def prt(board: str, text = None):
    isSmall = lambda n:"EX" if n == '-1' else ' '+n if (int(n) < 10) else  n
    board = ''.join(map(isSmall,board.split(',')))
    print('',board[:6])
    print('',board[6:12],end = '')
    print(' [{}]'.format(text))
    print('',board[12:18])
    print('','------')

class get_num:
    def __init__(self,board):
        self.board = board

    def change(self,br: str, now_pos: int, next_pos: int):
        br = br.split(',')
        br[now_pos],br[next_pos] = br[next_pos],br[now_pos]
        return ','.join(br)

    def Truedirections(self,br: str):
        br = br.split(',') # str -> list
        num_pos = []
        for i in range(len(br)):
            if not int(br[i]): num_pos.append(i)
        br = ','.join(br) # list -> str
        result = []
        rule = lambda n: bool(n not in ['-1','0']) # 출구,공백
        for pos in num_pos: # pos: int
            if pos not in list(range(3)) and rule(pos-3):
                result.append(self.change(br,pos,pos-3))
            if pos not in list(range(6,10)) and rule(pos+3):
                result.append(self.change(br,pos,pos+3))
            if pos not in list(range(0,7,3)) and rule(pos-1):
                result.append(self.change(br,pos,pos-1))
            if pos not in list(range(2,9,3)) and rule(pos+1):
                result.append(self.change(br,pos,pos+1))
        return result

    def isDone(self,br: str, num: int):
        br = br.split(',')
        num_pos = br.index(str(num))
        return (num_pos not in [5,7])

    def BFS(self,br: str, target: int):
        marked = {br:'start'}
        que = deque()
        que.append(br)
        node = que[0]
        while self.isDone(node,target):
            node = que.popleft()
            for connect_nodes in self.Truedirections(node):
                if connect_nodes not in marked:
                    marked[connect_nodes] = node
                    que.append(connect_nodes)
        marked['arrival'] = node
        return marked

    def recoding(self,marked: dict):
        start = ''.join([i for i, j in marked.items() if j == 'start'])
        arrival = ''.join([j for i, j in marked.items() if i == 'arrival'])
        node = arrival
        recode = []
        while node != start:
            recode.append(node)
            node = marked[node]
        return recode[::-1]

    def main(self, target: int):
        prt(self.board,'start')
        marked = self.BFS(self.board,target)
        recode = self.recoding(marked)
        if recode: self.board = recode[-1]
        for count,i in enumerate(recode):
            prt(i,count+1)
        return recode[-1] if recode else None

case3 = get_num('2,0,3,16,1,4,3,8,-1')
for i in converting_Bn(11)[::-1]:
    case3.main(i)

