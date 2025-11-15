def prt(br: str):
    print_ = lambda a: print('',a)
    print_('|'.join(br[:6]))
    print_('|'.join(br[6:12]))
    print_('|'.join(br[12:18]))
    print_('|'.join(br[18:24]))

def Truedirections(br: str, pos: int):
    pass

def unfolding(br: str, copy: str):
    node = br.index('1')        

def finding_path(br: str):
    pass

br = '290901800080909993000039'
copy_br = ''.join([str(br[i]) if br[i] in ['0','9'] else '0' for i in range(24)])
unfolding(br,copy_br)


