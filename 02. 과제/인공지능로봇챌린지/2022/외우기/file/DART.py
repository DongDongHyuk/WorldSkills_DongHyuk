drl_report_line(OFF)
printf = lambda *n: tp_log(' '.join(map(str,n)))

set_velx(2500); set_accx(1800); begin_blend(25)

device = sub_program_run('device') 
write,read = device.write,device.read
socket = sub_program_run('socket')

def posing(n,y,x):
    Len = y * x
    pos = [n] * Len 
    for i in range(1,Len):
        pos[i] = (trans(pos[i - 1],[-40,0,0,0,0,0]) if i % x else
                     trans(pos[i - x],[0,40,0,0,0,0]))
    return pos
    
pos_A = posing(None,6,4)
pos_B1 = posing(None,4,3)
pos_B2 = posing(None,3,4)
pos_C = [None,None]
pos_D = [None,None]
pos_index = None
positions = [pos_A,pos_B1,pos_B2,pos_C,pos_D,pos_index]

up_value = [[0,0,35,0,0,0],[0,0,5,0,0,0]]
up = lambda pos,n=None: trans(pos,[[0,0,n[0],0,0,0],[0,0,n[1],0,0,0]][isgrip] if n != None else up_value[isgrip])
Turn = lambda pos,n: [pos[0],pos[1],pos[2],[90,135,45,0,-90,180][n],180,0]

isgrip = 0
def grip(n):
    global isgrip
    if n == isgrip: 
    	return -1
    mwait(0)
    set_tool_digital_outputs([1*n,2*-n])
    wait(0.25)
    isgrip = 0 if n == -1 else 1
    
it_li = lambda: [read(i) for i in range(52,60)]
def it(n,t = 0.5):
    if not n: 
        return -1
    write(80 if n > 0 else 81,abs(n))
    wait(t*abs(n))
  
def gantry(n):  
    write(82,n)
    wait(0.8)

pack = 0
def moveg(Type,pos,up_val = None,device = True,angle=0): 
    global pack
    Pos = Turn(positions[Type][pos],angle) if Type != 5 else positions[Type]
    movel(up(Pos,up_val))
    movel(Pos)
    grip(-1 if isgrip else 1)
    if device:
        if isgrip: 
            pack = read(pos,Type)
        isexit = 20 if read(pos,Type) >= 20 else 0
        if not isexit and pack >= 20: 
        	pack -= 20
        write(pos,(0 if isgrip else pack)+isexit,Type)
    movel(up(Pos,up_val))

def get_board():
    br_A = [0,None,None,None,None]
    br_B = [1,None,None,None,None]                 
    n = lambda n,Type=0: read(n,Type)
    br_A[1] = ''.join(['0' if n(i) >= 20 else 'x' if n(i) == 9 else str(n(i)) for i in range(24)])
    br_A[2] = ''.join(['3' if n(i) == 2 else str(n(i)) for i in range(52,60)])
    br_A[3],br_A[4] = [i for i in range(24) if n(i) >= 20]
	    
    br_B[1] = [''.join(['1' if 10 < n(j) < 15 else 'x' if n(j) == 9 else '0' for j in range(24+i,36+i)]) for i in [0,12]]
    br_B[2] = [n(br_B[1][i].index('1'),i+1)-11 for i in range(2)]
    br_B[3] = [br_B[1][i].index('1') for i in range(2)]
    br_B[4] = [[j-(24+i) for j in range(24+i,36+i) if n(j) >= 20][0] for i in [0,12]]
    return [br_A,br_B]
    
def get_result(value):
    A_result = socket.open_server(value[0])
    B_result = socket.open_server(value[1])
    return [A_result,B_result]    
    
def Run_D():
    for i in range(2):
        for j in range(4):
            n = (20 * i) + j
            if read(n) >= 20:
                moveg(0,n,[35,85])
                moveg(4,i,[35,85],False)
    
def Run_A(result):
    for i in range(len(result)):
        s,e,turn,spin_count,pack,dire = result[i]
        it(spin_count)
        if spin_count: 
        	write(51,0)
        pack = 2 if pack == '12' else 1
        up_value = [35,35] if pack == 2 and dire in [1,3,5,7] else [35,5]
        angle = (1 if dire in [3,7] else 2)  if pack == 1 and dire in [1,3,5,7] else 0
        moveg(0,s,up_value)
        if angle: 
            movel(Turn(up(pos_A[s]),angle))
            movel(Turn(up(pos_A[e]),angle))
       	moveg(0,e,up_value)
        write(51,turn)
        
def loading_pack(pack):
    def amove_home():
        amovej([90,0]*3,200,200)
        wait(0.5)
    for j in range(2):
        gantry(pack)
        dire = it_li().index(pack)
        turn_ct = [(dire+i)%8 for i in range(8)].index(4)
        it(-(8-turn_ct) if turn_ct > 4 else turn_ct)
        amove_home()
        moveg(5,0,[35,85],False)
        write(56,0)                
        amove_home()
        
        movel(up(pos_A[A_road[0]],[0,85]))
        for i in A_road:
            movel(up(pos_A[i],[0,5]))
        movel(up(pos_A[A_road[-1]],[0,85]))
        
        for i in range(2):
            movel(pos_C[not(i)])
            grip(1 if i else -1)
            write(pack-1,0 if i else pack,3)
            if not i:
                 gantry(pack + 2)
        movel(up(pos_C[0],[0,85]))
            
        pos_B = [pos_B1,pos_B2][j]
        pos = br_B[3 if pack == 1 else 4][j]        
        movel(up(pos_B[pos],[0,100]))
        if pack == 1:
            n = read(pos,j+1) - 10
            angle = [4,5,0,3][n-1]
        else: 
            angle = 0
        movel(trans(Turn(pos_B[pos],angle),[0,0,0 if pack == 1 else 60,0,0,0]))
        grip(-1)
        write(pos,n if pack == 1 else 25,j+1)
        movel(Turn(up(pos_B[pos],[100,0]),angle))
        amove_home()
            
def Run_B(result):
    for i in range(len(result)):
        B1,B2,pack_dire,move_dire = result[i]
        write(50,move_dire+1)
        for j in range(2):
            s,e = [B1,B2][j]
            if None in [s,e]:
                continue
            moveg(j+1,s)
            angle = [0,3,4,5][move_dire]
            spin_value = [0,-90,-180,90][move_dire]
            time = [0,1.2,1.5,1.2][move_dire]
            moveg(j+1,e,None,False,angle)
            val = (pack_dire[j]+1) + (20 if e == br_B[4][j] else 0)
            write(e,val,j+1)
            amovej([0,0,0,0,0,spin_value], 200, 200, mod = 1)
            wait(time)                

# main

br_A,br_B = get_board()
A_result,B_result = get_result([br_A,br_B])
A_road,A_result = A_result
printf('done !!!')

while read(98) == 0:
    pass
write(98,0)

Run_D()
Run_A(A_result)
loading_pack(1)
Run_B(B_result)
loading_pack(2)

write(99,1)

from DRCF import *

w = '5 0 0 W S S 0 1 0 6 % D W 0 0 0 0 0 0 0 4'.split()
r = '5 0 0 R S S 0 1 0 6 % D W 0 0 0 4'.split()
w[0],r[0] = [5] * 2
w[-1],r[-1] = [4]  * 2

for i in [w,r]:
    i[1:-1] = map(ord,i[1:-1])
    
def write(ad,val,n=0):
    ad += [0,24,36,48][n]
    ser = serial_open(port = 'COM')
    w[13] = ord(str(ad//100))
    w[14] = ord(str((ad%100)//10))
    w[15] = ord(str(ad%10))
    w[18] = ord('0') if val < 16 else ord(hex(val)[2])
    w[19] = ord(hex(val)[2]) if val < 16 else ord(hex(val)[3])
    ser.write(bytearray(w))
    serial_close(ser)
    wait(0.02)
    
def read(ad,n=0):
    ad += [0,24,36,48][n]
    ser = serial_open(port = 'COM')
    r[13] = ord(str(ad//100))
    r[14] = ord(str((ad%100)//10))
    r[15] = ord(str(ad%10))
    ser.write(bytearray(r))
    wait(0.02)
    n = int(ser.read(ser.inWaiting()).decode()[10:14],16)
    serial_close(ser)
    return n
        
from DRCF import *

def open_server(value, port = 20001):
    Sock = server_socket_open(port)
    server_socket_write(Sock, str(value).encode('utf-8'))
    result = eval(server_socket_read(Sock,timeout = -1)[1].decode('utf-8'))
    server_socket_close(Sock)
    return result
