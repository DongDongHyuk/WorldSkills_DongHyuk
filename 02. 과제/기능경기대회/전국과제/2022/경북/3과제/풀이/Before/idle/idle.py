from collections import deque
from printer import prt
import time
      
def chn(board: str, now: int , new: int ):
      br = list(board) # str -> list
      br[now],br[new] = br[new],'0'
      return ''.join(br) # list -> str
    
def Truedirs(br: str):
      result = []
      n_p = [i for i in range(len(br)) if br[i] == '0' and i not in fix[1]]
      def rule(br,pos,posN):
            if Type in [0,2]:
                  return br[posN] not in fix[0] and posN not in fix[1] # fix pack,fix index
            if Type == 1:
                  if not(br[posN] not in fix[0] and posN not in fix[1]): return False # fix pack,fix index 
                  # 2층 안의 위치에 팩을 옮길때 위치 아래에 팩이 있어야됨
                  if pos >= 9 and br[pos-9] == '0': return False
                  # 1층에 있는 팩을 옮길떄 그 위치에 위에 팩이 있으면 안됨
                  if posN < 9 and br[posN+9] != '0': return False                  
                  return True                  
      rapd = result.append      
      if Type == 0: # Type 'A'
            for p in n_p:
                  for i in [-1,1,-3,3]:
                        if 0 <= p + i <= 8 and rule(br,p,p + i):
                              rapd(chn(br,p,p + i))
                              
      if Type == 1: # Type 'B'
            defult_Dirs = (-x_size,x_size,-1,1) # 상 하 좌 우
            for pos in n_p:
                  Wall = wall[pos >= 9]
                  for f in range(2): # there floor,other floor
                        n = (-9 if pos >= 9 else 9) if f else 0
                        for i,Dir in enumerate(defult_Dirs):
                              if pos not in Wall[i] and rule(br,pos,(pos+Dir)+n):
                                    rapd(chn(br,pos,(pos+Dir)+n))
      if Type == 2: # Type 'C'
            Dir = (-x_size,x_size,-1,1) # 상 하 좌 우
            for pos in n_p:
                  for i in range(4):
                        if pos not in wall[i] and rule(br,pos,pos+Dir[i]):
                              rapd(chn(br,pos,pos+Dir[i]))
      return result
                  
def bfs(root,leaf=None,idx=None,pack=None,goal_count=None):
      que = deque([root])
      marked = {root:'root'}
      br = root
      def isleaf(br): # 단말 노드일때 거짓 리턴
            if Type == 0:
                  return br != leaf
            if Type == 1:
                  if idx != None:
                        if pack != None: return br[idx] != pack
                        return br[idx] != leaf[idx]
                  if goal_count != None:
                        count = 0
                        for i in range(18):
                              if br[i] != leaf[i]: count += 1
                        return goal_count != count
                  return br != leaf
            if Type == 2:
                  if idx != None:
                        return br[idx] != leaf[idx]
                  return br != leaf
      while isleaf(br):
            br = que.popleft() # 현재 노드 
            for next_br in Truedirs(br):
                  if next_br not in marked:
                        marked[next_br] = br
                        que.append(next_br)
      marked['leaf'] = br
      if idx != None:fix[1].add(idx)
      return marked

def path(marked):
      br = marked['leaf'] # 이전 탐색의 단말 노드
      path = [br]
      while marked[br] != 'root':
            br = marked[br]
            path.append(br)
      return path[::-1]

def main(r:'root',l:'leaf',T: 'Types of Parets'):
      #Global Variables
      global root,leaf,Type,fix,wall,x_size # 고정,벽,오차
      root,leaf,Type = r,l,T
      fix = ({'0','x'},set()) # 고정 팩,고정 인덱스
      wall = [None,
            (({0,1,2},{6,7,8},{0,3,6},{2,5,8}),
            ({9,10,11},{15,16,17},{9,12,15},{11,14,17})),
            ({0,1,2,3},{12,13,14,15},{0,4,8,12},{3,7,11,15})][T]
      x_size = [None,3,4][T]      
      result = []

      start = time.time() # Start 
      
      if T == 0: # Type 'A'
            result = path(bfs(root,leaf)) # defult_bfs

      if T == 1: # Type 'B'
            marked,n_p = {'leaf':root},[]
            
            for pos in range(9):
                  if leaf[pos] == '0':
                        n_p.append(pos)
                        continue
                  marked = bfs(marked['leaf'],leaf,pos)
                  result += path(marked)
                  
            for i in range(2):
                  Dir,Wall,pack = [-3,3,-1,1],wall[n_p[i] >= 9],None
                  for j in range(4):
                        if n_p[i] not in Wall[j] and leaf[(n_p[i]+Dir[j])+9] not in fix[0]:
                              n = leaf[(n_p[i]+Dir[j])+9]
                              if i and n == marked['leaf'][n_p[0]]: continue
                              pack = n
                              break
                  marked = bfs(marked['leaf'],leaf,n_p[i],pack)
                  result += path(marked)                  
            marked = bfs(marked['leaf'],leaf,None,None,4)
            result += path(marked)
            
            fix[1].clear() # fixed index reset
            fix[1].update([i for i in range(18) if marked['leaf'][i] == leaf[i]]) # fix index update            
            marked = bfs(marked['leaf'],leaf)
            result += path(marked)

      if T == 2: # Type 'C'
            center,n = None,leaf.index('x') % 4
            for i in [5,6,9,10]:
                  if leaf[i] != 'x':
                        if n in [0,3]:
                              if not(n == 0 and i in [6,10]) and not(n == 3 and i in [5,9]):
                                    center = i
                                    break
                        else:
                              center = i
                              break
            sorting_pos,n = [center + i for i in [0,-5,-4,-3,-1,1,3,4,5]],leaf.index('x')           
            if n in [5,6,9,10]:
                  sequence = {5:[0,1,4],6:[3,2,7],9:[12,8,13],10:[15,11,14]}[n]
            else: sequence = []
            li = {5:[3,12,15,7,13,11,14],6:[0,15,12,4,14,8,13],
                  9:[0,15,3,1,11,2,7],10:[3,12,0,2,8,1,4]}
            sequence += [i for i in li[center] if i not in sequence]
            sequence = [i for i in sequence if i not in sorting_pos]
            marked = {'leaf':root}
            for i in sequence:
                  marked = bfs(marked['leaf'],leaf,i)
                  result += path(marked)
            marked = bfs(marked['leaf'],leaf)
            result += path(marked)

      end = time.time() # End

      for ct,board in enumerate(result):
            prt(board,ct)
      print('--',round(end - start,5),'second--')
      
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

      result = converter(result)
      print(result)
      return result
      
            
# M A I N

##root = '0213x5460'
##leaf = '5026x3041'
##Type = 0

root = '13524x060'+'13524x060' # 1,2 floor
leaf = '02316x450'+'05643x120'
Type = 1

##root = '451203x662041053'
##leaf = '150615x642034203'
##Type = 2 

main(root,leaf,Type)
