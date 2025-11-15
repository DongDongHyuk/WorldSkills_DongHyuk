import time as t
s = m = h = 0
while True:
    s += 1
    t.sleep(1)
    if s == 60:
        m += 1
        s = 0
    if m == 60:
        h += 1
        m = 0
    print('\n'*40)
    print("%dH %dM %dS" % (h,m,s))
        
