import random
from printer import printf

def rdm(y,x,n):
    s = y * x
    pack = '123456789abcdefg'
    m = list(pack[:n] + '0' * (s - n))
    random.shuffle(m)
    return ''.join(m)

