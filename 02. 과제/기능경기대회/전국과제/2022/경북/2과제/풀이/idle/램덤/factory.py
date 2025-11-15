from randomboard import *
from printer import *
from main import *
import time as t

ct = 0
while 1:    
    root,leaf = get_case(3)
    print('',"\n {} case(3,'{}','{}')".format(ct,root,leaf))   

    t_start = t.time()    
    res = main(3,root,leaf)
    t_end = t.time() - t_start

    print('','sorted' if res[-1] == leaf else 'not sorted',
          'in {}s'.format(round(t_end,5)))

    ct += 1
    
##    if input(" printing ? y or n \n -> ") == 'y':
##        for i in res:
##            printf(i,[4,4])
##
##    input('enter')

# 정리하고 무빙 ㄱ
