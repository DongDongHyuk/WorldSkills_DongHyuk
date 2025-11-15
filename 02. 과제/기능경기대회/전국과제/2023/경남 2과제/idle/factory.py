from rdm import rdm
from time import time
import main


t = 2 # <- map Type
loop_limit = 500000

ct,SUM_step,SUM_time,MAX_step,MAX_time = 0,0,0,0,0
def print_case():
    print("[{}] | {},'{}','{}',{}".format(ct,t,m1,m2,a))
def print_info():
    AVG_step,AVG_time = SUM_step // ct,SUM_time / ct        
    print('Step :',AVG_step,end = '/')
    print(MAX_step)
    print('Time : {}s(dart {}m {}s)'.
          format(round(AVG_time,6), int((AVG_time*250)//60), int((AVG_time*250)%60)),end = '/')
    print('{}s(dart {}m {}s)'.
          format(round(MAX_time,6), int((MAX_time*250)//60), int((MAX_time*250)%60))) 
while 1:
    m1,m2,a = rdm(t)
    ts = time()
    try:
        res = main.main(t,m1,m2,a)
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
    print('\n☆★☆★☆★☆★☆★☆\n★  COMPLETED !!!  ★\n☆★☆★☆★☆★☆★☆')

##    t,m1,m2,a = 1,'605a0709038400c0b201','60c50903a0020871040b',[4, 6, 12]          # hmi 예시 배치
##    t,m1,m2,a = 1,'090004200b78a001356c','0b3501006a9c08720004',[0, 4, 7]           # 거리가 멈    
##    t,m1,m2,a = 1,'359b01040000c6802a07','5103460b97080c2a0000',[18, 10, 6]         # 막힘
##    t,m1,m2,a = 1,'0000c250630148ab9070','530240a00700018bc096',[2, 17, 7]          # 홀에 막힘
##    t,m1,m2,a = 1,'68007030005004cb92a1','20b90700a60003814c50',[11, 7, 12]         # 가져오는길 막힘(구)
##    t,m1,m2,a = 1,'b069a3c0007082005140','a40130b028700c000569',[14, 11, 7]         # 가져오는길 막힘(신)
##    t,m1,m2,a = 1,'04053706100280a0c90b','6a05890c004100b27300',[18, 9, 6]          # 간접적으로 막힘(구)
##    t,m1,m2,a = 1,'a20814050976000b003c','b492000007a500680c13',[13, 16, 6]         # 간접적으로 막힘(신)
##    t,m1,m2,a = 1,'3c80b2000a1605047009','857100006b300c0490a2',[7, 17, 12]         # 화려하게 막힘
