from collections import deque
from printer import prt
import time

class IDS:
      def __init__(self,br,goal_br):
            self.br,self.goal_br = br,goal_br
            self.graph = {'A':['B','C','D'],
                          'B':['E','F'],
                          'C':[],
                          'D':['G','H'],
                          'E':[],
                          'F':['I','J'],
                          'G':['K'],
                          'H':[],
                          'I':[],
                          'J':[],
                          'K':[],}
            
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
            
      def iterative_dfs(self):
            depth = 1
            while 1:
                  marked = self.dfs(0,depth)
                  
                  if marked:
                        print('Found')
                        return marked
                  
                  depth += 1
                  #print('Maxdepth :',depth)
            return None

      def dfs(self,depth,Maxdepth):
            br,g_br = self.br,self.goal_br # 현재 보드, 도착 보드
            stack,marked = [br],{br:'start'}
            
            while not (depth == Maxdepth):
                  br = stack.pop()
                  
                  if br == g_br: # 목표보드를 찾음
                        return marked
                  
                  for node in self.Truedirs(br):
                        if node not in marked:
                              marked[node] = br
                              stack.append(node)
                  depth += 1
                  
            return False # 최대 깊이에 도달
                        

      def path(self,marked):
            br = self.goal_br
            path = [br]
            while marked[br] != 'start':
                  br = marked[br]
                  path.append(br)
            return path[::-1]

      def main(self):
            marked = self.iterative_dfs()
            result = self.path(marked)
            return result

if __name__ == '__main__':

      br = '267340015'
      goal_br = '123456700'

      case1 = IDS(br,goal_br)

      start = time.time()
      result = case1.main()
      end = time.time() - start

      exit(print(len(result)))
      for ct,i in enumerate(result):
             prt(i,ct+1)
        
      print('idle: {}초'.format(round(end,5)))
