'''
# 쓰레드
import threading as trd

def f1():
      for i in range(100):
            print(i,'\n')

def f2():
      for i in range(100,200):
            print(i)

trd.Thread(target=f1).start()
trd.Thread(target=f2).start()
'''

'''
from functools import lru_cache
import sys

sys.setrecursionlimit(10000)

# 캐싱
@lru_cache(maxsize = 2 ** 20)
def fibo(n):
      if n == 1 or n == 2:
            return 1
      else:
            return fibo(n - 1) + fibo(n - 2)

print(fibo(2000))
'''
import numba as nb

def fibo(n):
      if n == 1 or n == 2:
            return 1
      else:
            return fibo(n - 1) + fibo(n - 2)

run = nb.jit(fibo)

