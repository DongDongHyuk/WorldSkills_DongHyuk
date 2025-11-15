from queue import PriorityQueue
from printer import prt
import time

class Node: # 한 개의 노드의 보드,비용,휴리스틱,평가
      goal,kind = '',-1 # goal,board kind
      y,x,idx = 4,[5,5,6][kind],None # y,x,goal idx
      
      def __init__(self, board: str,moves: int = 0):
            self.board = board # 보드
            self.moves = moves # 움직임 횟수
      
      def __lt__(self, other): # 우선순위 큐에서 동점을 없앰
            return self.f() < other.f() # 평가가 낮을 수록 우선

      def f(self): # 평가 *낮을수록 평가가 좋음
            return self.g() + self.h()

      def g(self): # 비용
            return self.moves

      def h(self): # 휴리스틱 
            br,result = self.board,0
            td = lambda z: [z // self.x, z % self.x] # 1d -> 2d
            
            pos = td(br.index(self.goal[self.idx]))            
            goal = td(self.idx)
            
            result += abs(goal[1]-pos[1]) + abs(goal[0]-pos[0])            
            return result

class Best_First_Search:
      def __init__(self,node: 'class'):
            self.node = node # root node
            self.goal,self.kind = Node.goal,Node.kind # goal state,kind
            self.y,self.x = Node.y,Node.x # y,x
            self.holding = [] # holding indexs
            
      def bestfs(self):
            que = PriorityQueue() # 우선순위 큐
            que.put(self.node) # 루트 노드 추가
            marked = {self.node.board: None} # 방문 기록 생성, 루트 노드 추가
            self.idx = Node.idx # goal_idx
            
            while que: # 큐가 비어있을때 까지
                  br = que.get() # 우선순위 큐에서 시작 노드를 뻄                  
                  if br.board[self.idx] == self.goal[self.idx]:
                        self.node = br # 마지막 노드를 루트 노드로 변경
                        if self.idx != None:self.holding.append(self.idx) # 인덱스 고정
                        return marked                  
                  for node in self.Truedirs(br): # 우선순위 큐에서 빼낸 노드의 자식 노드
                        if node.board not in marked: # 만약에 자식노드에 방문하지 않았으면
                              marked[node.board] = br.board # 방문 체크
                              que.put(node) # 우선순위 큐에 추가                             
            return exit(print('Not Found')) # 목표노드를 찾지 못함 

      def chn(self, node: 'class', now, new):
            br = list(node.board) # 노드 클래스의 보드를 받음
            br[now],br[new] = br[new],'0'
            return Node(''.join(br), node.moves + 1) # 다른 보드를 가진 노드 클래스 return

      def Truedirs(self,node: 'class'):
            result = []
            num_pos = [ct for ct,i in enumerate(node.board) if i == '0']
            dy,dx = [-1,1,0,0],[0,0,-1,1]
            for pos in num_pos:
                  y,x = pos // self.x,pos % self.x
                  for i in range(4):
                        ny,nx = y + dy[i], x + dx[i]
                        nz = ny*self.x+nx
                        if 0 <= ny < self.y and 0 <= nx < self.x :
                              if nz not in self.holding and node.board[nz] not in ['0','X']:
                                    result.append(self.chn(node,pos,ny*self.x+nx))
            return result

      def path(self,marked):
            path = []
            node = self.node.board
            while marked[node] != None:
                  path.append(node)
                  node = marked[node]
            return path[::-1]

if __name__ == '__main__':

      root = Node('75XX1203040670204051XX63')
      goal = '73XX3762002650000541XX14'
      kind = 2
      
      Node.goal,Node.kind = goal,kind   
      case1 = Best_First_Search(root)

      sum_marked = 0 # marked sum
      Node.idx = 18
      
      marked = case1.bestfs()
      sum_marked += len(marked)
      print(sum_marked)
      Path = case1.path(marked)  
      
      for ct,node in enumerate(Path):
            prt(node,ct+1)

#start = time.time() # time
#end = time.time() - start # time
#print('idle: {}초'.format(round(end,5)))
