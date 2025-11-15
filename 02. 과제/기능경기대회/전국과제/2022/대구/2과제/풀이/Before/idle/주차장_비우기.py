# ''.join(map(str,list)) list -> str
# str(list) str -> list
from collections import deque
import random

def prt(board: str,num = None):
    br = ' '.join([' ' if not int(i) else '*' if i is '3' else i for i in board])
    print('',br[:8], end = '')
    print('  ','[{}]'.format(num))
    print('',br[8:16])
    print('',br[16:24])
    print('',br[24:32])
    print('---------')

class BFS:
    def __init__(self,board: str):
        self.br = board[:]

    def change(self,br:str,now_pos:int,next_pos:int):
        br = list(br)
        br[now_pos],br[next_pos] = br[next_pos],'0'
        return ''.join(br)

    def next_nodes(self,br):
        result = []
        num_pos = [ct for ct,i in enumerate(br) if not int(i)]
        rule = lambda posN: br[posN] not in [('-1'if self.mode else'9'),'0']
        for pos in num_pos:
            if pos not in list(range(4)) and rule(pos-4):
                result.append(self.change(br,pos,pos-4)) # up
            if pos not in list(range(12,16)) and rule(pos+4):
                result.append(self.change(br,pos,pos+4)) # down
            if pos not in list(range(0,13,4)) and rule(pos-1):
                result.append(self.change(br,pos,pos-1)) # letf
            if pos not in list(range(3,17,4)) and rule(pos+1):
                result.append(self.change(br,pos,pos+1)) # right
        return result
 
    def bfs(self,Exit):
        que = deque()
        que.append(self.br)
        marked = {self.br:'start'}
        node = None # index range Error
        def isDone(node):
            if not node: return not node
            if self.mode:
                num_pos = [ct for ct,i in enumerate(node) if not int(i)]
                return Exit not in num_pos # 비워야할 위치
            else: return node.index('3') != Exit
        while isDone(node):
            node = que.popleft()
            for next_node in self.next_nodes(node):
                if next_node not in marked:
                    marked[next_node] = node
                    que.append(next_node)
            if (not que): exit(print('unsolved !!!'))
        marked['arrival'] = node
        return marked

    def recoding(self,marked):
        node = marked['arrival']
        recode = [node]
        while marked[node] != 'start':
            node = marked[node]
            recode.append(node)
        return recode[::-1]
    
    def escape_parking_1(self,Exit,mode: '0:EFP 1:Resolt'):
        self.mode = mode
        marked = self.bfs(Exit)
        for ct,node in enumerate(self.recoding(marked)):
            prt(node,ct)

    def escape_parking_2(self,Exit,mode: '0:EFP 1:Resolt'):
        self.mode = mode
        marked = self.bfs(Exit)
        recode = self.recoding(marked)
        def convert(recode):
            new_recode = []
            for i in range(len(recode)-1):
                if i+1 > len(recode): break
                now_0_pos = [j for j in range(16) if not int(recode[i][j])]
                next_0_pos = [j for j in range(16) if not int(recode[i+1][j])]
                end = [i for i in now_0_pos if i not in next_0_pos]
                start = [i for i in next_0_pos if i not in now_0_pos]
                new_recode.append((start[0],end[0]))
            return new_recode
        return convert(recode)       

result = BFS('1290392210112090')
randomExit = random.randrange(3,16,4)
result.escape_parking_1(11,1)


