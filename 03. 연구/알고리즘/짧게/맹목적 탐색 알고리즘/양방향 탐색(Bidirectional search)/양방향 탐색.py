from collections import deque
from printer import prt
import time

class Bdr_search:
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
                        if 0 <= ny < 3 and 0 <= nx < 3 and br[ny*3+nx] != '0':
                              result.append(self.chn(br,pos,ny*3+nx))
            return result      

      def bfs_bdr(self):
            que = deque([self.br,self.goal_br])
            mkd_right,mkd_left = {self.br:'start'},{self.goal_br:'end'}
            Dir = {self.br:'right',self.goal_br:'left'}

            while que:
                  br = que.popleft()                                    
                  if br in mkd_right and br in mkd_left:
                        self.intersection_node = br
                        self.max_marked = len(mkd_right) + len(mkd_left)
                        return mkd_right,mkd_left #exit(print(len(mkd_left),len(mkd_right)))
                  for node in self.Truedirs(br):
                        if Dir[br] == 'right' and node not in mkd_right:
                              Dir[node] = 'right'
                              mkd_right[node] = br
                              que.append(node)                              
                        if Dir[br] == 'left' and node not in mkd_left:
                              Dir[node] = 'left'
                              mkd_left[node] = br
                              que.append(node)
                  
            return exit(print(len(mkd_left)))      

      def path(self,marked):
            br = self.intersection_node
            path = [br]
            while marked[0][br] != 'start':
                  br = marked[0][br]
                  path.append(br)            
            br = self.intersection_node
            path1 = [br]
            while marked[1][br] != 'end':
                  br = marked[1][br]
                  path1.append(br)
            return path[::-1] + path1[1:]                  

      def main(self):
            marked = self.bfs_bdr()
            result = self.path(marked)
            return result            

if __name__ == '__main__':

        br = '136207045'
        goal_br = '123456700'

        case1 = Bdr_search(br,goal_br)

        start = time.time()
        result = case1.main()
        end = time.time() - start
        
        for ct,i in enumerate(result):
              prt(i,ct+1)
              
        print('idle: {}초'.format(round(end,5)))
        print(case1.max_marked)
