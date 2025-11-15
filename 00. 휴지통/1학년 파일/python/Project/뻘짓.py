shape = "┼┼┼"

a = [shape]+[""]*29
b = [""]*29+[shape]
while True:
    for o in range(2):
        for i in range(1, 31) if o==0 else range(30, 0, -1):
            a[a.index(shape)] = ""
            a[i-1] = shape
            b[b.index(shape)] = ""
            b[i-1] = shape
            print(a)
            print(b)
        

