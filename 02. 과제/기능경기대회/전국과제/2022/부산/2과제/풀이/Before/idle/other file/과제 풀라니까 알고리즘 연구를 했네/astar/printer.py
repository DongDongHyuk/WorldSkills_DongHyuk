def prt(br: str,num = None):
    h,v = [(5,4),(6,4)][len(br) == 24]
    br = ' '.join([i.upper() for i in br])
    print('',br[:h*2])
    print('',br[h*2:h*4],end = '')
    print('  [{}]'.format(num))
    print('',br[h*4:h*6])
    print('',br[h*6:h*8])
    print('','---------' if h < 5 else '-----------')
