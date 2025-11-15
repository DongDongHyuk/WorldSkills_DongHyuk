from collections import deque
from printer import prt
import time

class 부산2과제:
    def __init__(self,br_kind,br,goal_br = None):
        self.br_kind = ['A','B','C'].index(br_kind) # 보드 종류
        self.br,self.goal_br = br,goal_br
        self.hold_li = []
        if self.br_kind == 1:
            self.p = br.index('g') # 궁 위치
            self.p_li = [self.p + i for i in [-6,-5,-4,1,6,5,4,-1]] # 궁 주변 인덱스 값
        if self.br_kind == 2:
            self.num_li = []
            self.idx_li = [[0,6,12,18,1,19,7,13],[5,11,17,23,4,22,10,16]]
            
    def chn(self, br, now, new): # new 위치의 팩을 now로 가져옴
        br = list(br)
        br[now],br[new] = br[new],'0'
        return ''.join(br)

    def Truedirs(self, br):
        result = []        
        n_p = [ct for ct,i in enumerate(br) if i == '0' and ct not in self.hold_li]        
        n = self.br_kind
        hold = [['0'],['g','0'],['0',' ']][n]
        W = [[(0,1,2,3,4),(15,16,17,18,19),(0,5,10,15),(4,9,14,19)],
            [(0,1,2,3,4,5),(18,19,20,21,22,23),(0,6,12,18),(5,11,17,23)]][n > 1]        
        val = [5,5,6][n]
        rapd = result.append 
        
        def rule(pos,posN):
            
            if self.br_kind == 0:
                if br[posN] in hold or posN in self.hold_li: return False                
                if br[posN] == 'h':
                    n = [-5,5,-1,1].index(posN - pos)
                    if posN not in W[n] and br[posN] != '0':
                        rapd(self.chn(br,pos,posN + (posN - pos)))                        
                    return False
                
            if self.br_kind == 1:
                dy,dx = [-1,1,0,0],[0,0,-1,1]

                # 바로 옆에 '포'가 있으면 False     
                if br[posN] == 'p': return False # 바로 옆에 '포'가 있으면 False
                
                # '수'는 궁 주위 8칸 안에서만 이동
                if br[posN] == 's' and pos not in self.p_li: return False

                # '마'는 직진후 대각이동 ***직진과 대각이동을 한 노드에 넣음                    
                if br[posN] == 'm':
                    posa,state = pos + (pos - posN),pos - posN
                    y,x = posa // 5, posa % 5
                    for i in [range(2,4),range(2)][state in [-1,1]]:
                        ny,nx = y+dy[i],x+dx[i]
                        nz = ny * 5 + nx
                        if 0 <= ny <= 3 and 0 <= nx <= 4 and br[nz] == '0':
                            rapd(self.chn(br,nz,posN))
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
                            if mode: rapd(self.chn(br,y*5+x,init[0]*5+init[1]))
                            else: return y*5+x                          
                        return posa(y,x,mode) # 탐색할 곳이 남음                    
                    Ny,Nx,state = posN // 5,posN % 5,posN - pos 
                    p_pos = posa(Ny,Nx,0) # '포'가 아닌 다른 기물에서 부터 탐색 시작                    
                    if p_pos is not None:
                        Ay,Ax,state = p_pos // 5, p_pos % 5, pos - posN
                        init = Ay,Ax #'포' 초기 위치 
                        posa(Ny,Nx,1) # '포'가 아닌 다른 기물에서 부터 탐색 시작
                        
                if br[posN] in hold or posN in self.hold_li: return False            
            return True
                    
        for pos in n_p:
            if pos not in W[0] and rule(pos, pos - val): rapd(self.chn(br,pos,pos-val)) # ↑           
            if pos not in W[1] and rule(pos, pos + val): rapd(self.chn(br,pos,pos+val))  # ↓          
            if pos not in W[2] and rule(pos, pos - 1): rapd(self.chn(br,pos,pos-1)) # ←  
            if pos not in W[3] and rule(pos, pos + 1): rapd(self.chn(br,pos,pos+1)) # →
            
        return result

    def bfs(self,idx = None):
        que = deque([self.br])
        br,g_br,kind = self.br,self.goal_br,self.br_kind
        marked = {self.br:'start'}
        def isDone(br):
            if self.br_kind == 0:
                if idx is not None: return br[idx] != g_br[idx]
                else: return br != g_br
                
            if self.br_kind == 1:
                li = list(map(lambda n:br[n],self.p_li))
                return li.count('0') != self.goal
            
            if self.br_kind == 2:
                if idx in [0,6,12,18,1,19,7,13]:
                    if br[idx] not in self.num_li:
                        self.num_li.append(br[idx])
                        return False
                    return True
                else: return br[idx] != self.goal_br[self.idx_li[1].index(idx)] 
                    
        while isDone(br):
            br = que.popleft()
            for next_br in self.Truedirs(br):
                if next_br not in marked:
                    marked[next_br] = br
                    que.append(next_br)
        self.br = br[:]
        self.hold_li.append(idx)
        return marked

    def path(self,marked):
        br = self.br
        path = [br]
        while marked[br] != 'start':
            br = marked[br]
            path.append(br)
        return path[::-1][1:] #출발지점 제외

    def main(self):
        result = []
        if self.br_kind == 0:
            for i in (0,1,2,3,4,5,6,10,11,15,16):
                marked = self.bfs(i)
                result.extend(self.path(marked))        
            marked = self.bfs()
            result.extend(self.path(marked))
            
        if self.br_kind == 1:
            #'차'고정,'궁'주변의 빈칸 갯수 
            self.hold_li,self.goal = [ct for ct,i in enumerate(self.br) if i == 'c'],2
            marked = self.bfs()
            result.extend(self.path(marked))
            #'차'가 아닌 기물 고정,'궁'주변의 빈칸 갯수
            self.hold_li,self.goal = [ct for ct,i in enumerate(self.br) if i not in ['c','0']],0 
            marked = self.bfs()
            result.extend(self.path(marked))
        
        if self.br_kind == 2:
            for idx in self.idx_li[0]:
                marked = self.bfs(idx)
                result.extend(self.path(marked))
            self.goal_br = list(map(lambda n: self.br[n],self.idx_li[0]))
            for idx in self.idx_li[1]:
                marked = self.bfs(idx)
                result.extend(self.path(marked))            
        return result        

#br = '0970h4d1a5b2h08600c3'
#goal_br = '103ahd804c60h70b5092'
 
br = 'm000c0s000p0gsmc000p'

#br = '75  1203040670204051  63'

case1 = 부산2과제('B',br)
start = time.time() # time_start
result = case1.Truedirs(br)
idle,dart = round(time.time() - start,3),round((time.time() - start)*300,3)
for ct,i in enumerate(result):
    prt(i,ct+1)

print('idle: {}초 | dart: {}초'.format(idle,dart))

#start = time.time() # time_start
#idle,dart = round(time.time() - start,3),round((time.time() - start)*100/60,3) # time_end    
#print('idle: {}초 | dart: {}분(s/60)'.format(idle,dart))

