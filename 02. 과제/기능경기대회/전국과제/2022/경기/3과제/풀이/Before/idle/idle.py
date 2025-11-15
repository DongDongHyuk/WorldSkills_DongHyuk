from collections import deque
from printer import prt
import time
      
def chn(board: str, now: int , new: int ):
      br = list(board) # str -> list
      br[now],br[new] = br[new],'0'
      return ''.join(br) # list -> str
    
def Truedirs(br: str): # sorting
      result = []
      n_p = [i for i in range(len(br)) if br[i] == '0' and i not in fix[1]]
      rule = lambda br,pos,posN: br[posN] not in fix[0] and posN not in fix[0]
      rapd = result.append
      Dir = (-x_size,x_size,-1,1) # 상 하 좌 우
      for pos in n_p:
            for i in range(4): # 상하좌우
                  if pos not in wall[i] and rule(br,pos,pos+Dir[i]):
                        rapd(chn(br,pos,pos+Dir[i]))
            if Type == 0: # 대각선
                  if pos not in wall[0] and pos not in wall[2] and rule(br,pos,pos -(x_size+1)):
                        rapd(chn(br,pos,pos -(x_size+1)))
                  if pos not in wall[0] and pos not in wall[3] and rule(br,pos,pos -(x_size-1)):
                        rapd(chn(br,pos,pos -(x_size-1)))
                  if pos not in wall[1] and pos not in wall[3] and rule(br,pos,pos +(x_size+1)):
                        rapd(chn(br,pos,pos +(x_size+1)))
                  if pos not in wall[1] and pos not in wall[2] and rule(br,pos,pos +(x_size-1)):
                        rapd(chn(br,pos,pos +(x_size-1)))
      return result

def Truedirs1(br,pos): # find_road
      result = []
      rule = lambda posN: br[posN] == '0'
      rapd = result.append
      Dir = (-x_size,x_size,-1,1) # 상 하 좌 우
      for i in range(4):
            if pos not in wall[i] and rule(pos + Dir[i]):
                  rapd(pos+Dir[i])
      if Type == 0: # A
            if pos not in wall[0] and pos not in wall[2] and rule(pos -(x_size+1)):
                  result.append(pos -(x_size+1))
            if pos not in wall[0] and pos not in wall[3] and rule(pos -(x_size-1)):
                  result.append(pos -(x_size-1))
            if pos not in wall[1] and pos not in wall[3] and rule(pos +(x_size+1)):
                  result.append(pos +(x_size+1))
            if pos not in wall[1] and pos not in wall[2] and rule(pos +(x_size-1)):
                  result.append(pos +(x_size-1))
      return result
                  
def bfs(root,leaf=None,idx=None): # sorting
      que = deque([root])
      marked = {root:'root'}
      br = root
      def isleaf(br): # 단말 노드일때 거짓 리턴
            if idx != None: return br[idx] != leaf[idx]
            return br != leaf
      while isleaf(br):
            br = que.popleft() # 현재 노드 
            for next_br in Truedirs(br): 
                  if next_br not in marked:
                        marked[next_br] = br
                        que.append(next_br)
      marked['leaf'] = br
      if idx != None: fix[1].add(idx)
      return marked

def bfs1(br,start,end): # find_road
      que = deque([start])
      marked = {start:'root'}
      pos = None
      while pos != end:
            pos = que.popleft()
            for next_pos in Truedirs1(br,pos):
                  if next_pos not in marked:
                        marked[next_pos] = pos
                        que.append(next_pos)
      marked['leaf'] = pos
      return marked

def path(marked):
      br = marked['leaf'] # 이전 탐색의 단말 노드
      path = [br]
      while marked[br] != 'root':
            br = marked[br]
            path.append(br)
      return path[::-1]

def main(r:'root',l:'leaf',T: 'Types of Parets',s: 'start'=None,e: 'end'=None ):
      #Global Variables
      global root,leaf,Type,fix,wall,x_size
      root,leaf,Type = r,l,T
      fix = ({'0','x'},set()) # 고정 팩,고정 인덱스
      wall = [({0,1,2,3},{20,21,22,23},{0,4,8,12,16,20},{3,7,11,15,19,23}),
            ({0,1,2,3,4,5},{18,19,20,21,22,23},{0,6,12,18},{5,11,17,23}),
            ({0,1,2},{9,10,11},{0,3,6,9},{2,5,8,11})][T]
      x_size = [4,6,3][T]  
      result = []

      if T in [0,1]:
            marked = {'leaf':root}
            result1,result2 = [],[] # sorting,find road
            # sorting
            if T == 0:
                  for i in (0,3,1,2,20,23,21,22):
                        marked = bfs(marked['leaf'],leaf,i)
                        result1 += path(marked)
                        prt(marked['leaf'],i)
                  marked = bfs(marked['leaf'],leaf)
                  result1 += path(marked)
            else:
                  marked = bfs(marked['leaf'],leaf)
                  result1 += path(marked)
            # find_road
            marked = bfs1(marked['leaf'],s,e)
            result2 = path(marked)
            result = [result1,result2] # result
            
            for i in range(len(result1)):
                  prt(result1[i],i)
            print('\n','Road :',result2)
            
      else: # C
            result = path(bfs(root,leaf))
            for i in range(len(result)):
                  prt(result[i],i)
                  
      # list -> index
      def converter(result):
            if not len(result): return []
            first,path = result[0],[]
            for second in result[1:]:
                  step = [None,None]
                  for i in range(len(second)):
                        if first[i] != second[i]:
                              if first[i] =='0': step[1] = i
                              else: step[0] = i
                  if None not in step: path.append(step)
                  first = second[:]
            return path
      
      if T in [0,1]:
            new_result = [converter(result[0]),result[1]] # sorting,find_road
      else: new_result = converter(result)
      print(new_result)
      return new_result
      
# M A I N

##root = '00300x3xx30300x0030030x0'
##leaf = '03000x0xx00003x3000333x0'
##Type = 0
##main(root,leaf,Type,0,0)

##root = '00300x3xx30300x0030030x0'
##leaf = '03000x0xx00003x3000333x0'
##Type = 1
##main(root,leaf,Type,0,0)

root = 'xx25140360xx'
leaf = 'xx01234560xx'
Type = 2
main(root,leaf,Type)

##start = time.time() # Start 
##end = time.time() # End
##print('--',round(end - start,5),'second--')


