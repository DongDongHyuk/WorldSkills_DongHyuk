from datetime import datetime

n = datetime.now()
print('')
print('┌─────────────────────┐')
print('│{} [{}]│'.format(n.date(),str(n.time())[:8]))
print('└─────────────────────┘\n')

def printf(br,y,x,z=1):
    br = ''.join([' ' if str(i) is 'x' else str(i) for i in br])
    for i in range(z-1,-1,-1):
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

# ○ Δ □ ● ▲ ■
# 1 2 3 4 5 6
