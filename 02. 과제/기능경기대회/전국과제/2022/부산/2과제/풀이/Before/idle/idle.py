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
                        if posN not in wall[Dir] and board[posN + (posN - pos)] not in ['0','h']:
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
                              if not 0 <= y <= 3 or not 0 <= x <= 4 or (not mode and board[y*5+x] in ['m','s','c','g']): return None
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
                  if board[posN] == 's' and pos not in g_li:return False
                  # '마'는 직진후 대각이동 ***직진과 대각이동을 한 노드에 넣음
                  if board[posN] == 'm':                        
                        posa,Dir = pos + (pos - posN),pos - posN
                        if pos in wall[[-5,5,-1,1].index(Dir)]: return False
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

def bfs(root: str,leaf = None,idx = None,score:'Distance Score' = None):
      que = deque([root])
      marked = {root:'root'}
      br = root
      def isleaf(br):            
            if Type == 0:                 
                  if idx != None: # idx
                        if leaf[idx] == '0':
                              idx_li = [i for i in range(20) if br[i] == '0' and i not in fix[1]]
                              Nscore = Scoring(idx_li[0],idx)  
                        else:Nscore = Scoring(br.index(leaf[idx]),idx)
                        return not Nscore < score  # 처음 점수와 비교하여 작으면 False                
                  return br != leaf # all            
            if Type == 1:
                  li = [br[i] for i in g_li]
                  return li.count('0') != leaf # leaf = 목표로 하는 궁 주위의 빈 칸 갯수            
            if Type == 2:
                  if leaf == 'push': return br[idx] == '0'
                  if leaf == None:
                        if br[idx] not in C1_li: # solting
                              C1_li.add(br[idx])
                              return False
                        return True
                  if leaf != None: return br[idx] != leaf
      while isleaf(br):
            br = que.popleft()
            for child_br in Truedirs(br):
                  if child_br not in marked:
                        marked[child_br] = br
                        que.append(child_br)
      marked['leaf'] = br
      if idx != None and score == None: fix[1].add(idx)
      return marked

def path(marked):
      br = marked['leaf'] # 이전 탐색의 단말 노드
      path = [br]
      while marked[br] != 'root':
            br = marked[br]
            path.append(br)
      return path[::-1][1:]

def main(r:'root',l:'leaf',T: 'Types of Parets'):
      #Global Variables
      global root,leaf,Type,fix,wall,val,g_li # 고정,벽,오차
      root,leaf,Type = r,l,T
      fix = [[{'0'},{'0','g'},{'0',' '}][Type],set(),[1,1,1,1]]
      wall = (({0,1,2,3,4},{15,16,17,18,19},{0,5,10,15},{4,9,14,19}),
             ({0,1,2,3,4,5},{18,19,20,21,22,23},{0,6,12,18},{5,11,17,23}))[Type > 1]
      val = (5,5,6)[Type]
      if Type == 1: g_li = [root.index('g') + i for i in (-6,-5,-4,1,6,5,4,-1)]
      result = []
      start = time.time() # Start      
      if Type == 0:
            global Scoring # main,bfs
            def Scoring(start,end):
                  start,end = (start//5,start%5),(end//5,end%5)
                  score = abs(start[0]-end[0]) + abs(start[1]-end[1]) # Distance Score
                  return score
            Sequence = (0,19,5,14,10,9,15,4,1,2,3)# 정렬 순서
            marked = {'leaf':root}
            for idx in Sequence:
                  print(idx)
                  if leaf[idx] == 'h':
                        fix[1].add(idx) # 수동 고정
                        continue
                  if leaf[idx] == '0':
                        idx_li = [i for i in range(20) if marked['leaf'][i] == '0' and i not in fix[1]]
                        score = Scoring(idx_li[0],idx)            
                  else: score = Scoring(marked['leaf'].index(leaf[idx]),idx)
                  for i in range(score,0,-1): # 현재 점수에서 1점까지                      
                        marked = bfs(marked['leaf'],leaf,idx,i)
                        result += path(marked)                        
                  fix[1].add(idx) # 수동 고정
            exit()
            result += path(bfs(marked['leaf'],leaf)) # 3 x 3 정렬 

      if Type == 1:
            marked = {'leaf':root}
            c_pos = [i for i in range(20) if root[i] == 'c']            
            for i in c_pos:
                  if i not in g_li:
                        fix[1].add(i)
                        break                  
            li = [marked['leaf'][i] for i in g_li]
            for i in range(li.count('0'),0,-1):
                  marked = bfs(marked['leaf'],i) # 궁 주변에 빈칸이 1개 일때   
                  result += path(marked)                  
            fix[1].clear() # 고정 없음
            result += path(bfs(marked['leaf'],0)) # 궁 주변에 빈칸이 없을때

      if Type == 2:
            global C1_li      
            def push(root,idx_li): # PUSH 
                  marked,Path = {'leaf':root},[]
                  for i in idx_li:
                        marked = bfs(marked['leaf'],'push',i)
                        Path += path(marked)
                  fix[1] -= set(idx_li) # 밀었던 인덱스 고정 해제
                  return Path,marked  
            # P U S H I N G
            Path,marked = push(root,(4,5,22,23,11,17,16,10,15,9,14,8))
            result += Path                  
            # C1구역에 각각다른 팩을 배치
            C1_li,li = set(),(1,0,6,12,18,19,7,13)
            for i in li:
                  marked = bfs(marked['leaf'],None,i)
                  result += path(marked)      
            # P U S H I N G
            Path,marked = push(marked['leaf'],(8,9,14,15))
            result += Path
            # C2구역에 대칭 배치
            for i in li:
                  j = i + (3 if i % 2 else 5) # 대칭 인덱스
                  marked = bfs(marked['leaf'],marked['leaf'][i],j)
                  result += path(marked)
                  
      end = time.time() # End

      # list -> index
      def converter(result):
            first,path = root,[]
            for second in result:
                  step = [None,None]
                  for i in range(len(second)):
                        if first[i] != second[i]:
                              if first[i] =='0': step[1] = i
                              else: step[0] = i
                  path.append(step)
                  first = second[:]
            return path
      #result = converter(result)
      
      # Result and Run time
##      for i in result: # step
##            print(i) 
      for n,board in enumerate(result): # board
            prt(board,n+1)
      
      print('--',round(end - start,5),'second--')  

# ====== M A I N ======

# input root and leaf

##root = '5800291hhb0acd476300'
##leaf = 'c0d397hh0804a601b205'
##
##main(root,leaf,0) # Runing Main.
##
root = 'm000c0s000p0gsmc000p'
root = '00m0c0g00mss000p00pc'
leaf = None

main(root,leaf,1) # Runing Main.
##
##root = '71  0706206501035044  23'
##leaf = None
##
###main(root,leaf,2) # Runing Main.

