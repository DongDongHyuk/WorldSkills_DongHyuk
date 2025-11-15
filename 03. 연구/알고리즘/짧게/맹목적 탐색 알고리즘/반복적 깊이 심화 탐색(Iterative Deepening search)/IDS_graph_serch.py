from collections import deque
from printer import prt
import time

class IDS:
      def __init__(self,graph,target):
            self.target = target
            self.graph = graph
            
      def iterative_dfs(self):
            depth = 1 # 깊이
            self.isBottom = False
            while not self.isBottom:
                  reuslt = self.dfs(0,depth) # 현재 깊이를 최대 깊이로 dfs
                  
                  if result: # 목표노드를 찾으면 값 리턴 
                        print('Found')
                        return result
                  
                  depth += 1 # 최대 깊이 +1 
                  
            return None # 목표를 찾지 못하고 최하단일때

      def dfs(self,depth,Maxdepth):
            # 일단 나중에 연구하시죠
            
            

if __name__ == '__main__':

      graph = {'A':['B','C','D'],
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

      case1 = IDS(graph,'I')

      start = time.time()
      result = case1.iterative_dfs()
      end = time.time() - start

      print(result)
        
      print('idle: {}초'.format(round(end,5)))
