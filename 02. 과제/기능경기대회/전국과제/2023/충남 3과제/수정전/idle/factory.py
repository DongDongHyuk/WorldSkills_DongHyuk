from rdm import rdm
from time import time
from main import main

t = 1 # <- map Type
loop_limit = 500000

ct,SUM_step,SUM_time,MAX_step,MAX_time = 0,0,0,0,0
def print_case():
    if t == 1:
        print("[{}] | {},'{}',{}".format(ct,t,m,li))
    if t == 2:
        print("[{}] | {},'{}'".format(ct,t,m))
def print_info():
    AVG_step,AVG_time = SUM_step // ct,SUM_time / ct        
    print('Step :',AVG_step,end = '/')
    print(MAX_step)
    print('Time : {}s(dart {}m {}s)'.
          format(round(AVG_time,6), int((AVG_time*250)//60), int((AVG_time*250)%60)),end = '/')
    print('{}s(dart {}m {}s)'.
          format(round(MAX_time,6), int((MAX_time*250)//60), int((MAX_time*250)%60)))    
while 1:
    if t == 1:
        m,li = rdm(1)
    if t == 2:
        m = rdm(t)
    ts = time()
    try:
        if t == 1:
            res = main(t,m,li)
        if t == 2:
            res = main(t,m)
    except:
        print('Failed Sorting')
        print_case()
        break
    te = time() - ts
    if te > MAX_time or len(res) > MAX_step:
        if te > MAX_time:
            MAX_time = te
        if len(res) > MAX_step:
            MAX_step = len(res)
        if ct:
            print_case()
            print_info()
            print('')    
    if ct > loop_limit:
        break
    SUM_step += len(res)
    SUM_time += te
    ct += 1    

if ct > loop_limit:
    print_info()
    print('\n☆★☆★☆★☆★☆★☆\n★  COMPLETED !!! ★\n☆★☆★☆★☆★☆★☆')
