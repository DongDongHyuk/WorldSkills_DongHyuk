def prt(br: str,num = None):
    br = ' '.join([' ' if i is '0' else 'X' if i is 'x' else i for i in br])    
    print('',br[:6])
    print('',br[6:12],'[{}]'.format(num))
    print('',br[12:])
    print('','-----')
