from collections import deque
from printer import prt
import time

class 부산2과제:
      def __init__(self,br_kind,br,goal_br):
            self.br_kind = ['A','B','C'].index(br_kind)
            self.br,self.goal_br = br,goal_br
            self.hold_idx = [] # C 
            self.num = [7,7] # C 

      def chn(self, br, now, new): # new 위치의 팩을 now로 가져옴
            br = list(br)
            br[now],br[new] = br[new],'0'
            return ''.join(br)

      def Truedir(self,br):
            n,result = self.br_kind,[]
            n_p = [ct for ct,i in enumerate(br) if i == '0']
            width = [5,5,6][self.br_kind]
            dy,dx = [-1,1,0,0],[0,0,-1,1]            
            hold = [[None],[None],['0','X',' ']][n]            
            for pos in n_p:
                  y,x = pos // width,pos % width
                  for i in range(4):
                        ny,nx = y + dy[i], x + dx[i]
                        nz = ny*width+nx
                        if 0 <= ny < 4 and 0 <= nx < width and br[nz] not in hold: 
                              if nz not in self.hold_idx:
                                    result.append(self.chn(br,pos,nz))
            return result

      def bfs_bdr(self):
            que = deque([self.br,self.goal_br])
            mkd_right,mkd_left = {self.br:'start'},{self.goal_br:'end'}
            self.Dir = {self.br:'right',self.goal_br:'left'}
            Dir = self.Dir
            while que:
                  br = que.popleft()
                  
                  if br in mkd_right and br in mkd_left:
                        print('\n','Find!!! marked:',len(mkd_right)+len(mkd_left),'\n')
                        self.intersection_node = br
                        return mkd_right,mkd_left
                  
                  for node in self.Truedir(br):
                        
                        if Dir[br] == 'right' and node not in mkd_right:
                              Dir[node] = 'right'
                              mkd_right[node] = br
                              que.append(node)
                              
                        if Dir[br] == 'left' and node not in mkd_left:
                              Dir[node] = 'left'
                              mkd_left[node] = br
                              que.append(node)
                              
            return exit(print('Not Found !!!'))     

      def path(self,marked):
            path = [[],[]]
            for i in range(2):
                  br = self.intersection_node
                  path[i].append(br)
                  while marked[i][br] != ['start','end'][i]:
                        br = marked[i][br]
                        path[i].append(br)                  
            return path[0][::-1] + path[1][1:]                  

      def main(self):
            marked = self.bfs_bdr()
            result = self.path(marked)
            return result            

if __name__ == '__main__':
            
      br = '75  1203040670204051  63'
      goal_br = '67  76'+'300003'+'210012'+'54  45'

      prt(br,'C','start_state')
      prt(goal_br,'C','end_state')

      case1 = 부산2과제('C',br,goal_br)

      start = time.time()
      result = case1.main()
      end = time.time() - start

      for ct,i in enumerate(result):
            prt(i,'C',ct+1)
              
      print('idle: {}초'.format(round(end,5)))
            
            
