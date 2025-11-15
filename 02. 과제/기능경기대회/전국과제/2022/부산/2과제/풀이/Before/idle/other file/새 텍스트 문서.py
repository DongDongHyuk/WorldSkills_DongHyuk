from collections import deque
from printer import prt
import time

class State:
    kind,hold_li = -1,[]
    root,leaf = '',''
    def __init__(self,br: str):
        self.board = br
        if State.kind == 1:
            State.p = br.index('g') # 궁 위치
            State.p_li = [State.p + i for i in [-6,-5,-4,1,6,5,4,-1]] # 궁 주변 인덱스 값
        
def chn(state: 'class', now, new): # new 위치의 팩을 now로 가져옴
    br = list(state.board)
    br[now],br[new] = br[new],'0'
    return State(''.join(br))

def Truedirs(state: 'class'):
    br,result = state.board,[]        
    n_p = [ct for ct,i in enumerate(br) if i == '0' and ct not in State.hold_li]        
    n = State.kind
    hold = [['0'],['g','0'],['0',' ']][n]
    W = [[(0,1,2,3,4),(15,16,17,18,19),(0,5,10,15),(4,9,14,19)],
        [(0,1,2,3,4,5),(18,19,20,21,22,23),(0,6,12,18),(5,11,17,23)]][n > 1]        
    val = [5,5,6][n]
    rapd = result.append
    def rule(pos,posN):            
        if State.kind == 0:
            if br[posN] in hold or posN in State.hold_li: return False                
            if br[posN] == 'h':
                n = [-5,5,-1,1].index(posN - pos)
                if posN not in W[n] and br[posN] != '0':
                    rapd(chn(state,pos,posN + (posN - pos)))                        
                return False            
        if State.kind == 1:
            dy,dx = [-1,1,0,0],[0,0,-1,1]
            # 바로 옆에 '포'가 있으면 False     
            if br[posN] == 'p': return False # 바로 옆에 '포'가 있으면 False            
            # '수'는 궁 주위 8칸 안에서만 이동
            if br[posN] == 's' and pos not in State.p_li: return False
            # '마'는 직진후 대각이동 ***직진과 대각이동을 한 노드에 넣음                    
            if br[posN] == 'm':
                posa,state = pos + (pos - posN),pos - posN
                y,x = posa // 5, posa % 5
                for i in [range(2,4),range(2)][state in [-1,1]]:
                    ny,nx = y+dy[i],x+dx[i]
                    nz = ny * 5 + nx
                    if 0 <= ny <= 3 and 0 <= nx <= 4 and br[nz] == '0':
                        rapd(chn(state,nz,posN))
                return False            
            # '포'는 '포'가 아닌 다른 기물을 넘어서 이동한다.
            if br[posN] not in ['p','0']:
                
                def posa(y,x,mode): # mode 0: finding '포' mode 1: finding '0'                        
                    for i in range(4): # 공백에서 기물을 바라본 방향으로 +1
                        if [-5,5,-1,1][i] == state:
                            y,x = y + dy[i], x + dx[i]
                            break
                    if not 0 <= y <= 3 or not 0 <= x <= 4: return None #못 찾음(탐색 범위 초과)                        
                    elif br[y*5+x] == ('0' if mode else 'p'): # 찾음
                        if mode: rapd(chn(state,y*5+x,init[0]*5+init[1]))
                        else: return y*5+x                          
                    return posa(y,x,mode) # 탐색할 곳이 남음
                
                Ny,Nx,state = posN // 5,posN % 5,posN - pos 
                p_pos = posa(Ny,Nx,0) # '포'가 아닌 다른 기물에서 부터 탐색 시작                    
                if p_pos is not None:
                    Ay,Ax,state = p_pos // 5, p_pos % 5, pos - posN
                    init = Ay,Ax #'포' 초기 위치 
                    posa(Ny,Nx,1) # '포'가 아닌 다른 기물에서 부터 탐색 시작
                    
            if br[posN] in hold or posN in State.hold_li: return False
            
        if State.kind == 2:
            if br[posN] in hold or posN in State.hold_li: return False            
        return True                
    for pos in n_p:
        if pos not in W[0] and rule(pos, pos - val): rapd(chn(state,pos,pos-val)) # ↑           
        if pos not in W[1] and rule(pos, pos + val): rapd(chn(state,pos,pos+val))  # ↓          
        if pos not in W[2] and rule(pos, pos - 1): rapd(chn(state,pos,pos-1)) # ←  
        if pos not in W[3] and rule(pos, pos + 1): rapd(chn(state,pos,pos+1)) # →            
    return result 

def bfs(idx = None):
    state,goal,kind = State.root,State.leaf,State.kind # root: class, leaf: str
    que = deque([state]) # put 'State' class
    marked = {state.board:'start'} # put 'State'.board
    def isDone(br):
        if State.kind == 0:
            if idx is not None: return br[idx] != goal[idx]
            else: return br != goal            
        if State.kind == 1:
            li = list(map(lambda n:br[n],State.p_li))
            return li.count('0') != goal        
        if State.kind == 2:
            return br[idx] != goal[idx]
    while isDone(state.board):
        state = que.popleft()
        for Cstate in Truedirs(state):
            if Cstate not in marked:
                marked[Cstate] = br
                que.append(Cstate)
    State.root = State(br[:])
    State.hold_li.append(idx)
    return marked

def path(marked):
    br = State.root
    path = [br]
    while marked[br] != 'start':
        br = marked[br]
        path.append(br)
    return path[::-1][1:] #출발지점 제외

def main():
    result = []
    if State.kind == 0:
        for i in (0,1,2,3,4,5,6,10,11,15,16):
            marked = bfs(i)
            result.extend(path(marked))        
        marked = bfs()
        result.extend(path(marked))        
    if State.kind == 1:
        #'차'고정,'궁'주변의 빈칸 갯수 
        State.hold_li,State.leaf = [ct for ct,i in enumerate(self.br) if i == 'c'],2
        marked = bfs()
        result.extend(path(marked))
        #'차'가 아닌 기물 고정,'궁'주변의 빈칸 갯수
        State.hold_li,State.leaf = [ct for ct,i in enumerate(self.br) if i not in ['c','0']],0 
        marked = bfs()
        result.extend(path(marked))    
    if State.kind == 2:
        exit()
    return result        

if __name__ == '__main__':
    
    #br = '0970h4d1a5b2h08600c3'
    #goal = '103ahd804c60h70b5092'
     
    br = 'm000c0s000p0gsmc000p'

    #br = '75  1203040670204051  63'

    State.root = State(br) # class
    State.leaf = goal # str
    State.kind = 0 # int
    result = main()

    for ct,i in enumerate(result):
        prt(i,ct+1)


#start = time.time() # time_start
#idle,dart = round(time.time() - start,3),round((time.time() - start)*100/60,3) # time_end    
#print('idle: {}초 | dart: {}분(s/60)'.format(idle,dart))

