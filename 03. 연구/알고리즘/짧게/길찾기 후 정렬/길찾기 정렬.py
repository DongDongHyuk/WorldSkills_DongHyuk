from printf import printf
from collections import deque
from queue import PriorityQueue

class State:
    def __init__(self, br, steps = 0):
        self.br = br
        self.steps = steps

    def __lt__(self, other):
        return self.f() < other.f()

    def f(self):
        return self.g() + self.h()

    def g(self):
        return self.steps

    def h(self):
        pass

def exc(state,now,new):
    # rules
    if state.br[new] not in fix[0] and new not in fix[1]
    br = list(state.br)
    br[now],br[new] = br[new],'0'
    return State(''.join(br),state.steps + 1)

def exp_sorting(state):
    global fix
    wall = [(0,1,2,3),(12,13,14,15),(0,4,8,12),(3,7,11,15)]
    Dir,fix = [-4,4,-1,1],[('0','x'),()]
    result = []
    n_p = [i for i in range(len(state.br)) if state.br[i] == '0']
    for pos in n_p:
        for i in range(4):
            if pos not in wall[i]:
                result.append(exc(state,pos,pos+Dir[i]))
    return result   

def exp_getdire(state):
    pass

if __name__ == '__main__':
    root = State('1234567890000000')
    for i in exp_sorting(root):
        printf(i.br,4,4)