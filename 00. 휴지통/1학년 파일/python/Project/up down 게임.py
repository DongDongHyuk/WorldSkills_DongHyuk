import random as r
import time as t
a = count = 0
r = r.randint(1,100)
while r != a:
    a = int(input('input int: '))
    count += 1
    print(a)
    if a == r:
        print('총 입력횟수: {}'.format(count))
    if a < r:
        print('up')
    if a > r:
        print('down')
    t.sleep(0.3)
