from datetime import datetime

n = datetime.now()
print('======================')
print('{} [{}]'.format(n.date(),str(n.time())[:8]))
print('======================')
print('')

def printf(br,height,width):        # 파레트 출력
    br = ' '.join([i for i in br])
    for i in range(height):
        print('',br[width*(i*2):width*((i+1)*2)])
    print('\n')

def prints(s,height,width):        # 파레트 출력
    br = ' '.join([i for i in s.br])
    for i in range(height):
        print('',br[width*(i*2):width*((i+1)*2)])
    print('\n','f({}) = g({}) + h({})'.format(s.h+s.step,s.step,s.h),'\n')
    print('======================','\n')