#set_velx(); set_accx()

buzz = lambda a: write(50,a)

def grip(n, ad = -1, val = -1):
    wait(0.1)
    set_tool_digital_outputs([1*n,2*-n])
    if -1 not in [ad,val]: write(ad,val)
    wait(0.05)

def moves(pos, ad = -1, val = -1):
        movel(trans(pos,up_pos[1]))
        movel(pos)
        grip(1, ad, val)

def movea(pos, ad = -1, val = -1, bz = -1):
        grip(-1, ad, val)
        if bz != -1: buzz(bz)
        movel(trans(pos,up_pos[1]))

def open_close(n):
    global B_2
    if B_2 == n: return -1
    B_2 = n
    moves(B[5-n], 40 - n, 0)
    movec(trans(B[4+n],[0,0,5,0,0,0]),trans(B[4+n],up_pos[0]),2000,1200)
    movea(B[4+n], 39 + n, 3, 2)

def up_down(n):
    _next = n - 1
    _now = B_1.index(1)
    if _next == _now: return
    open_close(1)
    moves(B[_now], 35 + _now, 0)
    movec(trans(B[_next], [0,0,5,0,0,0]),trans(B[_next],up_pos[0]),2000,1200)
    movea(B[_next], 35 + _next, 3)
    open_close(0)
    B_1[_next] = 3
    B_1[_now] = 0

def put_pack():
    for i in range(2):
        pack = A_1[1-i]
        if i == 0: movel(trans())

            
