from multiprocessing import Process

def func1():
    exit()

def func2():
    for i in range(10,20):
        print(i)

p1 = Process(target=func1)
p2 = Process(target=func2)

p1.start()
p2.start()
