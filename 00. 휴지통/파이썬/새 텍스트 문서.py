ser=serial_open('COM')
def ts(ad,m=[],y=0,x=0,b=1):
	if b:
		ad+=100*(T+1)
	k='00'+['R','W'][not y]+'SB06%DW'
	k=[ord(i) for i in k]
	n = len(m) if not y else y * x
	ad=[0]*(3-len(str(ad)))+list(map(int,str(ad)))
	k+=[ord(str(abs(i))) for i in ad]
	k+=[ord(i) for i in '{:02X}'.format(n)]
	if not y:
		for i in m:
			if i<0:
				i+=2**16
			k+=[ord(j) for j in '{:04X}'.format(i)]
	ser.write([5]+k+[4])
	wait(0.02 if n==1 else 0.05)
	k=ser.read(ser.inWaiting())
	if y:
		for i in range(0,y*x*4,4):
			n=int(k[10+i:14+i],16)
			if n&(2**15):
				n-=2**16
			m.append(n)
		return m if len(m) > 1 else m[0]
def write(*a,b=1):
	if isinstance(a[0],int):
		a = [a]
	for i,j in a:
		ts(i,[j] if isinstance(j,int) else j,b=b)
def read(ad,y=1,x=1):
	return ts(ad,[],y,x)