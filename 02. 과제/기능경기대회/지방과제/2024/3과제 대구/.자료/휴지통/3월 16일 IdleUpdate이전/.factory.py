from rdm import rdm
from time import time
from main import main
from printer import printf


t = 2 # <- map Type
loop_limit = 50000
#if if 정진건이 여자라면? 안죽고 남자면 진건계좌에 만원        
ct,SUM_step,SUM_time,MAX_step,MAX_time = 0,0,0,0,0
def print_case():
    if t < 2:
        print("[{}] | {},'{}','{}','{}'".format(ct,t,root,leaf,a))
    else:
        print("[{}] | {},'{}','{}'".format(ct,t,root,leaf))
def print_info():
    AVG_step,AVG_time = SUM_step // ct,SUM_time / ct        
    print('Step :',AVG_step,end = '/n')
    print(MAX_step)
    print('Time : {}s(dart {}m {}s)'.
          format(round(AVG_time,6), int((AVG_time*250)//60), int((AVG_time*250)%60)),end = '/')
    print('{}s(dart {}m {}s)'.
          format(round(MAX_time,6), int((MAX_time*250)//60), int((MAX_time*250)%60)))  
while 1:
    if t < 2:
        root,leaf,a = rdm(t)
        
    else:
        root,leaf = rdm(t)
    ts = time()
    try:
        if t < 2:
            res = main(t,root,leaf,a)
        else:
            res = main(t,root,leaf)
    except:
        print('Failed Sorting')
        printf(root,2,10)
        print(1)
        printf(leaf,2,10)
        print(2)
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
