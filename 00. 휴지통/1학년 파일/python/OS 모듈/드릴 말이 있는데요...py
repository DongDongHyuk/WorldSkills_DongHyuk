import os
import time as t 

Dir = os.getcwd()

print(Dir)

os.mkdir('선생님')

A = ['선생님','진지하게요','집가고싶어요']
a = b = 0
while True:
    t.sleep(1.5)
    if a < 2:
        os.rename(A[a],A[a+1])
        a += 1
    else:
        a = 0
        b += 1
        os.rename('집가고싶어요','선생님')
    if b == 5:
        os.system("shutdown /s /t 0")
