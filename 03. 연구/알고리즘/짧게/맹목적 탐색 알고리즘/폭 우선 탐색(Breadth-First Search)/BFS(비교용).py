from collections import deque
from printer import prt
import time
from functools import lru_cache

class BFS:
      def __init__(self,br,goal_br):
            self.br,self.goal_br = br,goal_br

      def chn(self, br, now, new):
            br = list(br)        
            br[now],br[new] = br[new],'0'
            return ''.join(br)

      def Truedirs(self,br):
            result = []
            num_pos = [ct for ct,i in enumerate(br) if i == '0']
            dy,dx = [-1,1,0,0],[0,0,-1,1]
            for pos in num_pos:
                  y,x = pos // 3,pos % 3
                  for i in range(4):
                        ny,nx = y + dy[i], x + dx[i]
                        if 0 <= ny < 3 and 0 <= nx < 3 and br[ny*3+nx]:
                              result.append(self.chn(br,pos,ny*3+nx))
            return result

      @lru_cache(maxsize=32)
      def bfs(self):
            que = deque([self.br])
            marked = {self.br:'start'}
            br,g_br = self.br,self.goal_br
            while 1:
                  if br == g_br:
                        self.max_marked = len(marked)
                        break
                  br = que.popleft()
                  for node in self.Truedirs(br):
                        if node not in marked:
                              que.append(node)
                              marked[node] = br
            return marked

      def path(self,marked):
            br = self.goal_br
            path = [br]
            while marked[br] != 'start':
                  br = marked[br]
                  path.append(br)
            return path[::-1]

      def main(self):
            marked = self.bfs()
            result = self.path(marked)
            return result

if __name__ == '__main__':

      br = '267340015'
      goal_br = '123456700'

      case1 = BFS(br,goal_br)

      start = time.time()
      result = case1.main()
      end = time.time() - start

      for ct,i in enumerate(result):
            prt(i,ct+1)
        
      print('idle: {}초'.format(round(end,5)))
      print(case1.max_marked)

