def prt(br: str,num = None):
    h,v = [(4,4),(3,3),(5,3)][[16,9,15].index(len(br))]
    br = ' '.join([i.upper() if h == 4 else i for i in br])
    print('│',br[:h*2].rstrip(),'│')
    print('│',br[h*2:h*4].rstrip(),'├',end = '')
    print('─┤ {} │'.format(num))
    print('│',br[h*4:h*6].rstrip(),'│')
    if v > 3:print('│',br[h*6:h*8],'│')
    print('├─' + ('──────┤' if h == 3 else '────────┤' if h == 4 else '──────────┤'))

