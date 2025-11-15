from collections import deque
from queue import PriorityQueue
import time
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from printer import *

class State:
    leaf = None
    size = [4,4]       # y,x
    fix_pack = ['0','x']
    def __init__(self,br,dists=dict(),p_pos=None,step=0):
        self.br = br

        # 팩 마다 목표 위치 까지 거리(Key : Pack | Value : Distance)
        self.dists = dists
        self.p_pos = p_pos
        self.H = self.h()

        self.step = step        # Cost

    def __lt__(self,other):
        return self.f() < other.f()

    def f(self):
        return self.g() + self.H

    def g(self):
        return self.step

    def h(self):
        h = 0
        br,size = self.br,self.size
        rng = [self.p_pos] if self.p_pos else range(len(br))
        for i in rng:
            pack = br[i]
            if pack not in State.fix_pack:
                y,x = i // size[1], i % size[1]
                g_pos = self.leaf.index(pack)
                ny,nx = g_pos // size[1], g_pos % size[1]
                dist = abs(x - nx) + abs(y - ny)
                self.dists[pack] = dist
        return sum(self.dists.values())

def exchange(state,now,new):
    br = list(state.br)
    br[now],br[new] = br[new],'0'
    dists = state.dists.copy()
    return State(''.join(br),dists,now,state.step + 1)

def expand(state):
    result = []
    pos_li = [i for i in range(len(state.br)) if state.br[i] == '0']
    dy,dx,size = [-1,0,1,0],[0,1,0,-1],state.size
    for i in pos_li:
        y,x = i // size[1],i % size[1]
        for j in range(4):
            ny,nx = y + dy[j], x + dx[j]
            nz = ny * size[1] + nx
            if -1 < ny < size[0] and -1 < nx < size[1] and state.br[nz] not in state.fix_pack:
                result.append(exchange(state,i,nz))
    return result

def A_star(root):
    que = PriorityQueue()
    que.put(root)
    marked = {root.br:'root'}
    while que:
        state = que.get()
        if state.br == state.leaf:
            break
        for new_state in expand(state):
            if new_state.br not in marked:
                marked[new_state.br] = state.br
                que.put(new_state)
    marked['leaf'] = state.br
    return marked

def Path(marked):
    state = marked['leaf']
    path = [state]
    while marked[state] != 'root':
        state = marked[state]
        path.append(state)
    return path[::-1]

t_start = time.time()

State.leaf = '123456x7000000x0'
marked = A_star(State('600070x0530041x2'))
result = Path(marked)

t_end = time.time() - t_start

y,x = State.size
for i in result:
    printf(i,y,x)

print('visited : {}'.format(len(marked)))
print('{}s'.format(round(t_end,5)))