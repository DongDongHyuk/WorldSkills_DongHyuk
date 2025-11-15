def prt(br: str,num = None):
    h,v = [(9,1),(3,3),(4,4)][[9,18,16].index(len(br))]
    p_name = {1:'○',2:'Δ',3:'□',4:'●',5:'▲',6:'■'}
    br = ' '.join([p_name[int(i)] if i != 'x' and int(i) in p_name else i for i in br])
    
    if h == 9: # A 
        print('\n',br,end = '')
        print('  [{}]'.format(num))

    if h == 3: # B
        print('\n',br[:h*2],'',br[h*6:h*8])
        print('',br[h*2:h*4],'',br[h*8:h*10],end = '')
        print('  [{}]'.format(num)) 
        print('',br[h*4:h*6],'',br[h*10:h*12])
        
    if h == 4: # C
        print('\n',br[:h*2])
        print('',br[h*2:h*4],end = '')
        print('  [{}]'.format(num))
        print('',br[h*4:h*6])
        print('',br[h*6:h*8])


##root = '13524x006'+'13524x006'
##leaf = '023160450'+'056430120'
##
##prt(root,'test')
