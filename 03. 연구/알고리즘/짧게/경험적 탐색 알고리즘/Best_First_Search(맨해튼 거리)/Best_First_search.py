from queue import PriorityQueue
from printer import prt
import time

class State: # 한 개의 노드의 보드,비용,휴리스틱,평가 
      goal = '' # 도착 노드
      node_count = 0

      def __init__(self, board: str, moves: int = 0):
            self.board,self.moves = board,moves # 보드,움직임 횟수
            State.node_count += 1            
            #prt(board,'node_count: {}'.format(State.node_count))
      
      def __lt__(self, other): # 우선순위 큐에서 동점을 없애주기 위함
            return self.f() < other.f() # 다른 노드 보다 평가가 낮은가

      def f(self): # 평가 *낮을수록 평가가 좋음
            return self.g() + self.h()

      def g(self): # 비용
            return self.moves

      def h(self): # 휴리스틱 
            result,size = 0,3
            for i in range(1,9):
                  n = self.goal[i]
                  goal_y = self.goal.index(n) % size
                  goal_x = self.goal.index(n) // size
                  br_y = self.board.index(n) % size
                  br_x = self.board.index(n) // size
                  result += abs(goal_x - br_x) + abs(goal_y - br_y)
            return result

class Best_First_Search:
      
      def bestfs(self,start: 'class',goal):
            que = PriorityQueue()
            que.put(start)
            marked = {start.board: None}
            while que:
                  br = que.get() # 우선순위 큐에서 시작 노드를 뻄
                  # 부모 노드 평가
                  #prt(br.board,'{} + {} = {}'.format(br.g(),br.h(),br.f()))                  
                  if br.board == goal: return marked # 목표 노드를 찾았을때                  
                  for node in self.Truedirs(br): # 우선순위 큐에서 빼낸 노드의 자식 노드
                        if node.board not in marked: # 만약에 자식노드에 방문하지 않았으면
                              marked[node.board] = br.board # 방문 체크
                              que.put(node) # 우선순위 큐에 추가
                              #자식 노드 평가
                              #prt(node.board,'{} + {} = {}'.format(node.g(),node.h(),node.f()))                              
            return exit(print('Not Found')) # 목표노드를 찾지 못함 

      def chn(self, state: 'class', now, new):
            br = list(state.board)        
            br[now],br[new] = br[new],'0'
            return State(''.join(br), state.moves + 1)

      def Truedirs(self,state: 'class'):
            result = []
            num_pos = [ct for ct,i in enumerate(state.board) if i == '0']
            dy,dx = [-1,1,0,0],[0,0,-1,1]
            for pos in num_pos:
                  y,x = pos // 3,pos % 3
                  for i in range(4):
                        ny,nx = y + dy[i], x + dx[i]
                        if 0 <= ny < 3 and 0 <= nx < 3 and state.board[ny*3+nx]:
                              result.append(self.chn(state,pos,ny*3+nx))
            return result

      def path(self,marked):
            path = []
            node = State.goal
            while marked[node] != None:
                  path.append(node)
                  node = marked[node]
            return path[::-1]

if __name__ == '__main__':
      
      start_node = State('136207045')
      State.goal = '123456700'
      
      case1 = Best_First_Search()
      start = time.time() # time
      marked = case1.bestfs(start_node,State.goal)
      end = time.time() - start # time
      Path = case1.path(marked)

      for ct,br in enumerate(Path):
            prt(br,ct+1)
      print('idle: {}초'.format(round(end,5)))
      print('visit:',len(marked))
