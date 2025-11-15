##from datetime import datetime

##n = datetime.now()
##print('')
##print('┌─────────────────────┐')
##print('│{} [{}]│'.format(n.date(),str(n.time())[:8]))
##print('└─────────────────────┘')
print('')
print('○ : me | ● : robot')

def printf(m,y=9,x=9,z = 1):
    code = {0:' ',1:'●',2:'○'}
    br = ''.join([code[i] if i in code else str(i) for i in m])
    for i in range(z):
        if z > 1:
            print('{} Floor'.format(i+1))
        print(''.join(['┌───',''.join(['┬───'] * (x - 1)),'┐']))
        for j in range(y):
            n = x * j
            print('│',' │ '.join(br[(0 + ((y * x) * i) + n):(x + ((y * x) * i) + n)]),'│')
            if j != y - 1:
                print(''.join(['├───',''.join(['┼───'] * (x - 1)),'┤']))
        print(''.join(['└───',''.join(['┴───'] * (x - 1)),'┘']))
    print('')

