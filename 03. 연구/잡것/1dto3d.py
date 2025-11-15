for i in range(18):
    y,x = (i // 3) % 3, i % 3
    z = int(i >= (3 * 3))
    print(x,y,z)
