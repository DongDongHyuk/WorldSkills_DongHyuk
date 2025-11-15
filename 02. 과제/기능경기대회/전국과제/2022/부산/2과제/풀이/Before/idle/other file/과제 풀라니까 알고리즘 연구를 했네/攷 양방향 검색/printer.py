def prt(br: str,kind,num = None):
    h,v = [(5,4),(5,4),(6,4)][['A','B','C'].index(kind)]
    br = ' '.join([i.upper() for i in br])
    print('',br[:h*2])
    print('',br[h*2:h*4],end = '')
    print('  [{}]'.format(num))
    print('',br[h*4:h*6])
    print('',br[h*6:h*8])
    print('','---------' if h < 5 else '-----------')


#br = '0970h4d1a5b2h08600c3'
#prt(br,'A')
