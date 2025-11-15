from bot_mk1 import put_doll
from printer import *

m = [0] * 81
turn = 1
while 1:
    if turn % 2:
        pos = int(input('you : '))
        m[pos] = 2
    else:
        pos = put_doll(m)
        print('bot :',pos)
        m[pos] = 1
    turn  += 1
    printf(m)
