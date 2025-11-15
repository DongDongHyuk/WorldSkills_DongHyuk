from collections import deque
from printer import prt
import time

def chn(board: str, now: int , new: int ):
      br = list(board) # str -> list
      br[now],br[new] = br[new],'0'
      return ''.join(br) # list -> str

def Truedirs(board: str):
      result = []      
      n_p = (ct for ct,i in enumerate(board) if i == '0' and ct not in fix[1])
      def rule(board,pos,posN):
            if Type == 0:
                  if board[posN] in fix[0] or posN in fix[1]: return False
                  if board[posN] == 'h':
                        Dir = (-5,5,-1,1).index(posN - pos)
                        if posN not in wall[Dir] and board[posN] != '0':
                              result.append(chn(board,pos,posN + (posN - pos)))
                        return False
                  return True
            if Type == 1:
                  dy,dx = [-1,1,0,0],[0,0,-1,1]
                  # '포'는 '포'가 아닌 다른 기물을 넘어서 이동한다.
                  if board[posN] not in ['p','0']:
                        def posa(y,x,mode):
                              for i in range(4):
                                    if [-5,5,-1,1][i] == state:
                                          y,x = y + dy[i], x + dx[i]
                                          break
                              if not 0 <= y <= 3 or not 0 <= x <= 4: return None
                              elif board[y*5+x] == ('0' if mode else 'p'):
                                    if mode: result.append(chn(board, y*5+x,init[0]*5+init[1]))
                                    else: return y*5+x
                              return posa(y,x,mode)
                        Ny,Nx,state = posN // 5,posN % 5, posN - pos
                        p_pos = posa(Ny,Nx,0)                        
                        if p_pos is not None:
                              Ay,Ax,state = p_pos // 5, p_pos % 5, pos - posN
                              init = Ay,Ax
                              posa(Ny,Nx,1)
                  # 바로 옆에 '포'가 있으면 False     
                  if board[posN] == 'p': return False # 바로 옆에 '포'가 있으면 False            
                  # '수'는 궁 주위 8칸 안에서만 이동
                  if board[posN] == 's' and pos not in p_li:return False
                  # '마'는 직진후 대각이동 ***직진과 대각이동을 한 노드에 넣음
                  if board[posN] == 'm':
                        posa,Dir = pos + (pos - posN),pos - posN
                        y,x = posa // 5, posa % 5
                        for i in [range(2,4),range(2)][Dir in (-1,1)]:
                              ny,nx = y+dy[i],x+dx[i]
                              nz = ny * 5 + nx
                              if 0 <= ny <= 3 and 0 <= nx <= 4 and board[nz] == '0':
                                    result.append(chn(board,nz,posN))
                        return False                              
                  if board[posN] in fix[0] or posN in fix[1]: return False                  
                  return True # 기물에 따른 조건이 모두 성립하면 True                  
            if Type == 2:
                  if board[posN] in fix[0] or posN in fix[1]: return False
                  return True
      for pos in n_p:
            if fix[2][0] and pos not in wall[0] and rule(board, pos, pos - val):
                  result.append(chn(board,pos,pos-val)) # ↑  
            if fix[2][1] and pos not in wall[1] and rule(board, pos, pos + val):
                  result.append(chn(board,pos,pos+val))  # ↓ 
            if fix[2][2] and pos not in wall[2] and rule(board, pos, pos - 1):
                  result.append(chn(board,pos,pos - 1)) # ←  
            if fix[2][3] and pos not in wall[3] and rule(board, pos, pos + 1):
                  result.append(chn(board,pos,pos + 1)) # →
      return result

def bfs(root: str,leaf = None,idx = None):
      que = deque([root])
      marked = {root:'root'}
      br = root
      def isleaf(br):            
            if Type == 0:
                  if not que and leaf == None: return False # Push
                  if idx != None: return br[idx] != leaf[idx]
                  else: return br != leaf
                  
            if Type == 1:
                  li = [br[i] for i in p_li]
                  return li.count('0') != leaf # leaf = 목표로 하는 궁 주위의 빈 칸 갯수
            
            if Type == 2:
                  if leaf == 'push': # pushing
                        return br[idx] == '0'
                  if leaf == None:
                        if br[idx] not in C1_li: # solting
                              C1_li.add(br[idx])
                              return False
                        return True
                  if leaf != None: # 'push'는 위에서 리턴
                        return br[idx] != leaf
                  
      while isleaf(br):
            br = que.popleft()
            for child_br in Truedirs(br):
                  if child_br not in marked:
                        marked[child_br] = br
                        que.append(child_br)
      marked['leaf'] = br
      if idx != None: fix[1].add(idx)
      return marked

def path(marked):
      br = marked['leaf'] # 이전 탐색의 단말 노드
      path = [br]
      while marked[br] != 'root':
            br = marked[br]
            path.append(br)
      return path[::-1][1:]

def main(root:str,leaf:str,Type: 'Types of Parets'):      
      result = []
      start = time.time() # Start
      
      if Type == 0:
            fix[2] = [1,0,0,0] # 아래로만 이동 가능
            marked = bfs(root,None) # P U S H I N G
            result.extend(path(marked))
            fix[2] = [1,1,1,1] # 방향 고정 없음
            for i in (0,1,2,3,4,5,10,15,6,11,16):
                  marked = bfs(marked['leaf'],leaf,i)
                  result += path(marked)            
            marked = bfs(marked['leaf'],leaf)
            result += path(marked)

      if Type == 1:
            fix[0].add('c') # '차' 고정
            marked = bfs(root,2)
            result += path(marked) # 궁 주변에 빈칸이 2개 일때            
            fix[0].update(['m','s','p']) # '차' 제외 모두 고정
            fix[0].remove('c')
            result += path(bfs(marked['leaf'],0)) # 궁 주변에 빈칸이 없을때

      if Type == 2:
            global C1_li
            def push2(root,idx_li):
                  marked,Path = {'leaf':root},[]
                  for i in idx_li:
                        marked = bfs(marked['leaf'],'push',i)
                        Path += path(marked)
                  fix[1].clear()
                  return Path,marked            
            # P U S H I N G
            Path,marked = push2(root,(4,5,22,23,11,17,16,10,15,9,14,8))
            result += Path                  
            # C1구역에 각각다른 팩을 배치
            C1_li,li = set(),(1,0,6,12,18,19,7,13)
            for i in li:
                  marked = bfs(marked['leaf'],None,i)
                  result += path(marked)      
            # P U S H I N G
            Path,marked = push2(marked['leaf'],(8,9,14,15))
            result += Path
            # C2구역에 대칭 배치
            fix[1].update(li) # push2에서 C1고정 풀린거 다시 고정하
            for i in li:
                  j = i + (3 if i % 2 else 5) # 대칭 인덱스
                  marked = bfs(marked['leaf'],marked['leaf'][i],j)
                  result += path(marked)
      end = time.time() # End
      
      # Result and Run time
      for n,board in enumerate(result):
            prt(board,n+1)
      print('--',round(end - start,5),'second--')  

# ====== M A I N ======

# input root and leaf

Type = 2

#root = '0970h4d1a5b2h08600c3'
#leaf = '103ahd804c60h70b5092'

#root = 'm000c0s000p0gsmc000p'
#leaf = None

root = '75  1203040670204051  63'
leaf = None

#Global Variables
fix = [[{'0'},{'0','g'},{'0',' '}][Type],set(),[1,1,1,1]]
wall = (({0,1,2,3,4},{15,16,17,18,19},{0,5,10,15},{4,9,14,19}),
       ({0,1,2,3,4,5},{18,19,20,21,22,23},{0,6,12,18},{5,11,17,23}))[Type > 1]
val = (5,5,6)[Type]
if Type == 1: p_li = [root.index('g') + i for i in (-6,-5,-4,1,6,5,4,-1)]

main(root,leaf,Type) # Runing Main.
