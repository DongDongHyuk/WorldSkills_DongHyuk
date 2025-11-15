from rdm import rdm
from time import time
from main import main


t = 0 # <- map Type
loop_limit = 10000

ct,SUM_step,SUM_time,MAX_time = 0,0,0,0
def print_case():
    if t == 0:
        print("[{}] | {},'{}','{}'".format(ct,t,m1,m2))
def print_info():
    if ct:
        AVG_step,AVG_time = SUM_step // ct,SUM_time / ct        
        print('Average Step :',AVG_step)
        print('Average Time : {}s(dart {}m {}s)'.
              format(round(AVG_time,6), int((AVG_time*250)//60), int((AVG_time*250)%60)))
        print('Maximum Time : {}s(dart {}m {}s)'.
              format(round(MAX_time,6), int((MAX_time*250)//60), int((MAX_time*250)%60)))    
while 1:
    if t == 0:
        m1,m2 = rdm(t)
    ts = time()
    try:
        if t == 0:
            res = main(t,m1,m2)
    except:
        print('Failed Sorting')
        print_case()
        break
    te = time() - ts
    if te > MAX_time:
        MAX_time = te
        print_case()
        print_info()
        print("{}step, idle {}s(dart {}m {}s)\n".
        format(len(res), round(te,6), int((te*250)//60), int((te*250)%60)))
    if te > 1 or ct > loop_limit:
        break
    SUM_step += len(res)
    SUM_time += te
    ct += 1
    
print_info()
if ct > loop_limit:
    print('COMPLETED.')
