from collections import deque
import datetime

def step():
    pass    

start = datetime.datetime.now()
main()
end = datetime.datetime.now()
h,m,s = str(end-start).split(":")
print("{}분 {}초".format(m,s))
