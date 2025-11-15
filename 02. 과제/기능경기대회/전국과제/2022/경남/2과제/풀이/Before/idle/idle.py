from collections import deque
from printer import prt
import time

def chn(board: str, now: int , new: int ):
      br = list(board) # str -> list
      if Type == 1: #is 'B' board
            now_pack = br[new] # 옮기는 팩
            mate_pack = now_pack.lower() if now_pack.isupper() else now_pack.upper() # 옮기는 팩의 메이트
            br[br.index(mate_pack)] = '0'
      if Type == 2:
            if br[new] == 'b': # isBridge
                  new = new + (new - now)
      br[now],br[new] = br[new],mate_pack if Type == 1 else '0'
      return ''.join(br) # list -> str      

def Truedirs(board: str):
      result = []
      n_p = [ct for ct,i in enumerate(board) if i == '0' and ct not in fix[1]]
      def rule(board,pos,posN):
            if Type == 0:
                  if board[posN] == 'p': # isPortal
                        Dir = (-4,4,-1,1).index(posN - pos)
                        posN + (posN - pos)
                        if posN not in wall[Dir] and board[posN + (posN - pos)] not in fix[0]:
                              result.append(chn(board,pos,posN + (posN - pos)))
                        return False           
            return posN not in fix[1] and board[posN] not in fix[0]
      for pos in n_p:
            if pos not in wall[0] and rule(board, pos, pos - val):
                  result.append(chn(board,pos,pos-val)) # ↑  
            if pos not in wall[1] and rule(board, pos, pos + val):
                  result.append(chn(board,pos,pos+val))  # ↓ 
            if pos not in wall[2] and rule(board, pos, pos - 1):
                  result.append(chn(board,pos,pos - 1)) # ←  
            if pos not in wall[3] and rule(board, pos, pos + 1):
                  result.append(chn(board,pos,pos + 1)) # →
      return result
      
def bfs(root: str,leaf=None,idx=None,A_type=None,score:'Distance Score' = None):
      que = deque([root])
      marked = {root:'root'}
      br = root
      def isleaf(br):
            if Type == 0: # 'A'
                  if leaf == 'porting':
                        return idx not in p_around_pack(br,A_type)
                  if idx is not None:
                        if score is not None:
                              Nscore = Scoring(br.index(leaf[idx]),idx)
                              return not Nscore < score
                        return br[idx] != leaf[idx]
                  return br != leaf
            if Type == 1: # 'B'
                  pack_li = [br.index(i) for i in ['A','B','C','a','b','c']]
                  A,B,C,a,b,c = pack_li
                  if 4 not in [B,b]: return True
                  if not((A - B) in [-3,3,-1,1] and (A - B) == (B - C)): return True
                  if not((a - b) in [-3,3,-1,1] and (a - b) == (b - c)): return True
                  return False
            if Type == 2: # 'C'
                  pack_li = lambda br:({br[i]for i in range(5)},{br[j]for j in range(10,15)})
                  a,b = pack_li(br)
                  return not('2' not in a and '1' not in b)
      while isleaf(br):
            br = que.popleft()
            for child_br in Truedirs(br):
                  if child_br not in marked:
                        marked[child_br] = br
                        que.append(child_br)
      marked['leaf'] = br
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
      global root,leaf,Type,fix,wall,val # 고정,벽,오차
      root,leaf,Type = r,l,T
      fix = ({'x','0'},set()) # 고정 팩,고정 인덱스
      wall = [({0,1,2,3},{12,13,14,15},{0,4,8,12},{3,7,11,15}),
              ({0,1,2},{6,7,8},{0,3,6},{2,5,8}),
              ({0,1,2,3,4},{10,11,12,13,14},{0,5,10},{4,9,14})][T]
      val = [4,3,5][T]
      start = time.time() # Start      
      result = []
            
      if T == 0: # A
            global p_pos,p_around,p_around_pack,Scoring
            p_pos = (root[0].index('p'),root[1].index('p')) # 포탈 위치          
            p_around = [[p_pos[0] + i for ct,i in enumerate([-4,4,-1,1]) if p_pos[0] not in wall[ct]]] # 포탈 위치 주변
            p_around.append([p_pos[1] + i for ct,i in enumerate([-4,4,-1,1]) if p_pos[1] not in wall[ct]])
            p_around_pack = lambda br,n: [br[i] for i in p_around[n]] # 포탈 주변 팩들(sync)            
            pack_li = [[i for i in root[0] if i not in ['x','p','0'] and i in leaf[1]]] # A1,A2 팩
            pack_li.append([i for i in root[1] if i not in ['x','p','0'] and i in leaf[0]])
            print(pack_li)
            def Scoring(start,end):
                  start,end = (start//4,start%4),(end//4,end%4)
                  score = abs(start[0]-end[0]) + abs(start[1]-end[1]) # Distance Score
                  return score
            result,result0,result1 = [[],[],[]],[],[]
            
            # 서로의 팩을 교환 해야됨
            marked0,marked1 = {'leaf':root[0]},{'leaf':root[1]}            
            def porting(n1:'del',n2:'add',num): # 보드에 팩 지우기
                  board1,board2 = [marked0['leaf'],marked1['leaf']][n1],[marked0['leaf'],marked1['leaf']][n2]
                  board1,board2 = list(board1),list(board2)
                  board1[board1.index(num)] = '0' # del
                  pos = p_around[n2][p_around_pack(board2,n2).index('0')]
                  board2[pos] = num # add
                  if n1: return ''.join(board2),''.join(board1)
                  return ''.join(board1),''.join(board2)
            
            marked0 = bfs(marked0['leaf'],'porting','0',0)
            result[0] = path(marked0)  # A1_board_setting
            for i,j in zip(pack_li[0],pack_li[1]): # porting
                  # A2 --> A1
                  marked1 = bfs(marked1['leaf'],'porting',j,1)
                  result1 += path(marked1)
                  marked0['leaf'],marked1['leaf'] = porting(1,0,j)
                  # A1 --> A2
                  marked0 = bfs(marked0['leaf'],'porting',i,0)
                  result0 += path(marked0)
                  marked0['leaf'],marked1['leaf'] = porting(0,1,i)                  
                  result[1].append([result1,result0]) # 팩을 서로 한개씩 교환한 상태에서 append
                  result0,result1 = [],[] # reset
                  
            for marked,Result,leaf in zip([marked0,marked1],[result0,result1],[leaf[0],leaf[1]]):
                  center = [i for i in [5,6,9,10] if marked['leaf'][i] != 'x']
                  sequence,num_ct = [],[]
                  for c in center:
                        li = [i for i in [0,15,3,12,4,11,8,7,13,1,14,2]]
                        li = [i for i in li if i not in list(map(lambda n:c+n,[-5,-4,-3,1,5,4,3,-1]))+[c]]
                        sequence.append(li)
                        num_ct.append([leaf[i] for i in li].count('0'))
                  sequence = sequence[num_ct.index(min(num_ct))]                  
                  for idx in sequence:
                        if leaf[idx] == '0': # 0 은 거리 점수X
                              marked = bfs(marked['leaf'],leaf,idx)
                              Result += path(marked)
                        else: # 0 을 제외한 팩은 거리 점수 O
                              score = Scoring(marked['leaf'].index(leaf[idx]),idx)
                              for i in range(score,0,-1):
                                    marked = bfs(marked['leaf'],leaf,idx,None,i)
                                    Result += path(marked)
                        fix[1].add(idx)
                  marked = bfs(marked['leaf'],leaf)
                  Result += path(marked)[1:]
                  result[2].append(Result)
                  fix[1].clear()
                              
      else: # B,C
            result += path(bfs(root,leaf)) # B,C
      
      end = time.time() # End

##      # Only A
##      for count,A1 in enumerate(result[0]):
##            prt(A1,count+1)
##      print('│ Setting │\n│   [↓]   │\n├─────────┤')            
##      for count,(A2,A1) in enumerate(result[1]):
##            for ct,i in enumerate(A2):
##                  prt(i,'A2 - {}'.format(ct+1))
##            print('│   [{}]   │\n│   [↓]   │\n├─────────┤'.format(count+1))            
##            for ct,j in enumerate(A1):
##                  prt(j,'A1 - {}'.format(ct+1))
##            print('├─────────┤')            
##      print('│ Porting │\n│   [↓]   │\n├─────────┤')
##      for count,A in enumerate(result[2]):
##            for ct,a in enumerate(A):
##                  prt(a,('A2' if count else 'A1')+' - {}'.format(ct+1))
            
      for count,board in enumerate(result): # B or C 
            prt(board,count) 

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

      def converter_1(result): # B 파레트 전용
            if not len(result): return []
            first,path = result[0],[]
            for second in result[1:]:
                  step = [None] * 4
                  for i in ['a','b','c']:
                        if first.index(i) != second.index(i):                              
                              step[0],step[1] = first.index(i),second.index(i)
                              pack_state = first.index(i.upper()) - step[0]
                              step[3] = second.index(i.upper()) - step[1]                              
                              if pack_state in [1,-1]: # 팩이 가로
                                    l,r = (-3,3) if pack_state == 1 else (3,-3)
                              else:
                                    l,r = (1,-1) if pack_state == 3 else (-1,1) # 세로                              
                              n1,n2 = first.index(i.upper()),first.index(i)
                              turn_dir = [n1+l,n1+r,n2+l,n2+r]                              
                              for j in range(4):
                                    if not(0 <= turn_dir[j] < 9):continue
                                    if second[turn_dir[j]] in [i,i.upper()]: step[2] = j                              
                  path.append(step)
                  first = second[:]
            return path
      
      if T == 0: # A result = [[A1_setting],[ [[[]*n],[[]*n]], * 9 ]
            setting_result = converter(result[0]) # setting
            porting_result = [] # porting
            for result1 in result[1]:
                  result2 = []
                  for result3 in result1:
                        result2.append(converter(result3))
                  porting_result.append(result2)
            solting_result = [] # solting
            for i in result[2]:
                  solting_result.append(converter(i))
            return [setting_result,porting_result,solting_result]
      
      if T == 1: # B
            result = converter_1(result)
            return result
      
      if T == 2: # C
            result = converter(result)
            return result

# Main

# A
##root = ('d30h90x00p5f1b07','60xcap042e800i0g')
##leaf = ('4g06eax00pi02c08','d9x51p00f00b7h30')
##root = ('bc4023001a50pxe0', '00i90dg0h870f6xp')
##leaf = ('009c05h4107fpxb0', '000306dgaie802xp')
##root = ('bc0a23401p500xe0', '00900diph8gx76f0')
##leaf = ('009c05h41p7f0xb0', '20036dgpaiex0008')
##
##Type = 0

# B
root = 'C00c0baAB'
leaf = None
Type = 1

#C
##root = '21020xxxbx01201'
##leaf = None
##Type = 2

main(root,leaf,Type) # Runing Main.





