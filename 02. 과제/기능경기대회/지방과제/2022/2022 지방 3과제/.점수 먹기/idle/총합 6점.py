set_velx(1000); set_accx(800)

begin_blend(10)



up_pos = [[0,0,1,0,0,0],[0,0,38,0,0,0]]

buzz = lambda a: write(100,a)

def grip(n, ad=-1,val=-1):
    wait(0.1)
    set_tool_digital_outputs([1*n,2*-n])
    if -1 not in [ad,val]: write(ad,val)
    wait(0.1)

def moves(pos, ad=-1,val=-1):
    movel(trans(pos,up_pos[1]))
    movel(pos)
    grip(1, ad,val)

def movea(pos, ad=-1,val=-1):
    grip(-1)
    movel(trans(pos,up_pos[1]))

def up_down(pos, ad=-1,val=-1):
    num = read(ad)
    moves(pos, ad, val)
    movel(trans(pos,up_pos[1]))
    movel(pos)
    movea(pos,ad,num)

def spin_index(n):
    for _ in range(n):
        write(80,1)
        box = it[0]
        del it[0]
        it.append(box)
        for i in range(1,9):
            write(i,it[i-1])

def main():
    up_down(A[0]) # 1 - 2
    spin_index()
