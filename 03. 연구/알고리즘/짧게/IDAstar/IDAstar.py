from collections import deque
from queue import PriorityQueue
import time
from printer import *

class State:
    leaf = None
    size = [None] * 2       # y,x
    fix_pack = ['0','x']
    
    def __init__(self,br,dists=dict(),p_pos=None,step=0):
        self.br = br

        # 팩 마다 목표 위치 까지 거리(Key : Pack | Value : Distance)
        self.dists = dists
        self.p_pos = p_pos

        self.step = step            # Cost
        self.h = self.get_h()       # heuristic

    def __lt__(self,other):
        return self.f() < other.f()

    def f(self):
        return self.step + self.h       # f = cost + heuristic

    def get_h(self):
        h = 0
        br,size = self.br,self.size

        rng = [self.p_pos] if self.p_pos else range(len(br))
        for i in rng:
            pack = br[i]
            if pack not in State.fix_pack:
                y,x = divmod(i,size[1])
                g_pos = State.leaf.index(pack)
                ny,nx = divmod(g_pos,size[1])
                dist = abs(x - nx) + abs(y - ny)
                self.dists[pack] = dist

        h += sum(self.dists.values())            
        
        conflict = 0

        for n in range(2):          # Now Searching line (Horizontal or vertical)
            for i in range(size[n]):
                inline = []
                for j in range(size[not n]):
                    p_pos = (j * size[1] + i) if n else (i * size[1] + j)
                    pack = br[p_pos]
                    if  pack != '0':
                        g_pos = State.leaf.index(pack)
                        ny,nx = divmod(g_pos,size[1])
                        if pack == 'x':
                            inline.append((pack,p_pos))
                        elif (nx if n else ny) == i:
                            inline.append((pack,p_pos,g_pos))
                            
                for j in inline:
                    for k in inline:
                        if j[0] == k[0]:
                            continue
                        if 'x' in [j[0],k[0]]:
                            if j[0] == 'x' and k[1] < j[1] < k[2]:
                                conflict += 1
                                continue
                            elif k[0] == 'x' and j[1] > k[1] > j[2]:
                                conflict += 1
                                continue
                        else:
                            if k[1] < j[1] and j[2] < k[2]:
                                conflict += 1

        h += 2 * conflict

        return h

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
        y,x = divmod(i,size[1])
        for j in range(4):
            ny,nx = y + dy[j], x + dx[j]
            nz = ny * size[1] + nx
            if  -1 < ny < size[0] and -1 < nx < size[1] and \
                state.br[nz] not in state.fix_pack:
                    result.append(exchange(state,i,nz))
    return result

def A_star(root):
    que = PriorityQueue()
    que.put(root)
    marked = [{root.br},{root:'root'}]
    while que:
        state = que.get()
        if state.br == state.leaf:
            break
        for new_state in expand(state):
            if new_state.br not in marked[0]:
                marked[0].add(new_state.br)
                marked[1][new_state] = state
                que.put(new_state)
    marked[1]['leaf'] = state
    return marked[1]

def Path(marked):
    state = marked['leaf']
    path = [state]
    while marked[state] != 'root':
        state = marked[state]
        path.append(state)
    return path[::-1]

if __name__ == '__main__':

    br_0 = ['1234'
            '5607'
            '00x8'
            '09ab'] 

    br_1 = ['6080'
            '70a9'
            '53xb'
            '4102']

    leaf,root = list(map(''.join,[br_0,br_1]))
    State.leaf,State.size = leaf,[4,4]

    # br = State('607000x8503041x2')
    # prints(br,4,4)

    t_start = time.time()
    marked = A_star(State(root))
    t_end = time.time() - t_start

    result = Path(marked)
    
    y,x = State.size
    for i in result:
        prints(i,y,x)

    print('','{} visited for {}s'.format(len(marked),round(t_end,5)))