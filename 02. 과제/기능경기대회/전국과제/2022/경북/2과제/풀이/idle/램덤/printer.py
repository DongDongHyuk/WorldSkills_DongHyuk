##from datetime import datetime

##n = datetime.now()
##print('')
##print('┌─────────────────────┐')
##print('│{} [{}]│'.format(n.date(),str(n.time())[:8]))
##print('└─────────────────────┘')
print('')

def printf(br,size):
    y,x = size
    print(''.join(['┌───',''.join(['┬───'] * (x - 1)),'┐']))
    for i in range(y):
        n = x * i
        print('│',' │ '.join(br[(0 + n):(x + n)]),'│')
        if i != y - 1:
            print(''.join(['├───',''.join(['┼───'] * (x - 1)),'┤']))
    print(''.join(['└───',''.join(['┴───'] * (x - 1)),'┘']))
    print('')
