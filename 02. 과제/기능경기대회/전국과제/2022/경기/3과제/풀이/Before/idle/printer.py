def prt(br: str,num = None):
    h,v = [(None,None),(None,None),(3,4)][[24,24,12].index(len(br))]
    if len(br) == 24:
        if br.count('x') == 4: h,v = 6,4 # B
        else: h,v = 4,6 # A
    br = ' '.join([i.upper() for i in br])
    
    if h == 4: # A 
        print('\n',br[:h*2])
        print('',br[h*2:h*4])
        print('',br[h*4:h*6],end = '')
        print('  [{}]'.format(num))
        print('',br[h*6:h*8])
        print('',br[h*8:h*10])
        print('',br[h*10:h*12])

    if h == 6 or h == 3: # B,C
        print('\n',br[:h*2])
        print('',br[h*2:h*4],end = '')
        print('  [{}]'.format(num))
        print('',br[h*4:h*6])
        print('',br[h*6:])



##board = 'x000x0300x030x0030300000'
##
##prt(board,'test')
