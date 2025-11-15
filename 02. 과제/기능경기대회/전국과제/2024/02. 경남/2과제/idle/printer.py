from datetime import datetime

n = datetime.now()
print('')
print('┌─────────────────────┐')
print('│{} [{}]│'.format(n.date(),str(n.time())[:8]))
print('└─────────────────────┘\n')

def printf(br,y,x,z=1,hli = []):
    b = [[7,8,1],[5,5,1],[1,5,3]].index([y,x,z])
    li = [[0,1,2,5,6,7,8,9,10,11,12,13,14,15,17,22,24,25,30,31,33,38,40,41,42,43,44,45,46,47,48,49,50,53,54,55],
          [1,3,5,9,12,15,19,21,23],[]][b]
    br = ''.join([' ' if str(br[i]) == 'x' and i in li else str(br[i]) for i in range(len(br))])
    br = ['H' if i in hli else br[i] for i in range(len(br))]
    # if not b:
    #     br[9],br[2],br[5],br[14] = '/','/','\\','\\'
    #     br[11],br[12],br[24],br[31],br[43],br[44] = ['│']*6
    #     br[41],br[50],br[46],br[53] = '\\','\\','/','/'
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
