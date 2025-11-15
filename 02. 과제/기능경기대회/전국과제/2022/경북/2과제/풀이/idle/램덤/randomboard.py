from printer import *
import random

def get_case(Type):
    sy,sx = [[3,3],[3,4],[3,4],[4,4]][Type]
    sz = sy * sx
    dy,dx = [-1,0,1,0],[0,1,0,-1]
    get_pos = lambda br: random.choice([i for i in range(sz) if br[i] == '0'])

    def get_br(fpp):
        br = ['0'] * sz if Type != 2 else list('x00x0000x00x')

        br[fpp] = 'x'
        
        while 'P' not in br:
            pos = (get_pos(br))
            y,x = divmod(pos,sx)
            for i in range(4):
                ny,nx = y + dy[i], x + dx[i]
                nz = ny * sx + nx
                if -1 < ny < sy and -1 < nx < sx and \
                    br[nz] == '0':
                    br[pos],br[nz] = 'P','p'
                    break
                
        li = [[2,6,7,9],
              [1,3,4,5,8],
              [2,7],
              [1,3,4,5,6,8,9]][Type]
        
        for i in list(map(str,li)):                
            br[get_pos(br)] = i

        return ''.join(br)

    fpp = random.choice([[0,1,2,3,5,6,7,8],[4,5,6,7],[1,2,4,7,9,10],list(range(16))][Type])
    br = get_br(fpp),get_br(fpp)

    return br
