printf = lambda li: tp_log("{}".format(li))
printl = lambda li: list(map(lambda a: print(a),li))
"""
w = '5 0 0 W S S 0 1 0 6 % D W 0 0 0 0 0 0 0 4'.split()
r = '5 0 0 R S S 0 1 0 6 % D W 0 0 0 4'.split()
w[0],r[0] = [5] * 2
w[-1],r[-1] = [4] * 2

for i in [w,r]:
    i[1:-1] = list(map(lambda a: ord(a),i[1:-1]))
    
def write(ad, val):
    ser = serial_open(port = 'COM')
    w[13] = ord(str(ad//100))
    w[14] = ord(str((ad%100)//10))
    w[15] = ord(str(ad%10))
    w[18] = ord(str(0)) if val < 16 else ord(hex(val)[2])
    w[19] = ord(hex(val)[2]) if val < 16 else ord(hex(val)[3])
    ser.write(bytearray(w))
    serial_close(ser)
    wait(0.02)
    
def read(ad):
    ser = serial_open(port = 'COM')
    r[13] = ord(str(ad//100))
    r[14] = ord(str((ad%100)//10))
    r[15] = ord(str(ad%10))
    ser.write(bytearray(r))
    wait(0.02)
    n = int(ser.read(ser.inWaiting()).decode()[10:14],16)
    serial_close(ser)
    return n
"""
it_pos = []
A = []
B_1 = []
B_2 = []
C_in = []
C_out = []
D = []

up_pos = [[0,0,10,0,0,0],[0,0,38,0,0,0],[0,0,65,0,0,0]]

it = [0,1,1,2,2,0,0,0] # 1 : 사각 2 : 원형

A_pal = [[9,9,9,9,9,9],
         [9]+[1,1,0,2]+[9],
         [9]+[9,0,0,0]+[9],
         [9]+[0,0,9,0]+[9],
         [9]+[0,9,0,0]+[9],
         [9]+[0,0,0,9]+[9],
         [9]+[2,0,1,1]+[9],
         [9,9,9,9,9,9]]

buzz = lambda a: write(50,a)

def grip(n, ad=-1, val=-1):
    wait(0.1)
    set_tool_digital_outputs([1*n,2*-n])
    if -1 not in [ad,val]: write(ad,val)
    wait(0.05)

def moves(pos,ad=-1,val=-1):
    movel(trans(pos,up_pos[1]))
    movel(pos)
    grip(1,ad,val)    

def movea(pos,ad=-1,val=-1):
    grip(-1, ad,val)
    movel(trans(pos,up_pos[1]))

def throw_pack():
    A_pos = [0,20]; D_pos = [0,1]
    for i in range(2):
        num = read(11+A_pos[i])
        moves(A[0], 11+A_pos[i], 0)
        movel(trans(A[A_pos[i]],up_pos[2]))
        movel(trans(A[D_pos[i]],up_pos[2]))
        movel(A[D_pos[i]])
        movea(A[D_pos[i]], 10+D_pos[i], num)    

def dire(n):
    y = [-1,-1,0,1,1,1,0,-1]
    x = [0,1,1,1,0,-1,-1,-1]
    result = []
    for i in range(8):
        if it[i] == n:
            result.append([y[i],x[i]])
    return result

def pos():
    for i in [1,2]:
        dr = dire(i)
        for y in [1,6]:
            for x in range(1,5):
                if A_pal[y][x] == i:
                    for j in dr: # [[-1,1],[0,1]]
                        if A_pal[y+j[0]][x+j[1]] == 0:
                            return[[y,x],[y+j[0],x+j[1]],A_pal[y][x],j] # 출발,도착,팩정보,방향

def apack_move(li):
    n1,n2,num,dire = li
    s = ((n1[0]-1)*4+n1[1])-1
    a = ((n2[0]-1)*4+n2[1])-1
    moves(A[s], 11+s, 0)
    movel(trans(A[s],up_pos[0]))
    if dire in [[-1,-1],[1,1]]: movel([0,0,0,-45,0,0],mod = 1)
    if dire in [[-1,1],[1,-1]]: movel([0,0,0,45,0,0],mod = 1)
    

def main():
    throw_pack() # 팩 버리기
    apack_move(pos())

main()      
