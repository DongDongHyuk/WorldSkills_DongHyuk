##from datetime import datetime

##n = datetime.now()
##print('')
##print('┌─────────────────────┐')
##print('│{} [{}]│'.format(n.date(),str(n.time())[:8]))
##print('└─────────────────────┘')
print('')

def printf(br,y,x,z = 1):
    code = {'0':' ','1':'○','2':'Δ','3':'□','4':'●','5':'▲','6':'■',}
    br = ''.join([code[i] if i in code else str(i) for i in br])
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

