import time as t
from tkinter import *

win = Tk()
win.geometry("500x750")
win.title("정수형 날 보고있다면 과제 좀 알려줘")
win.option_add("*Font","안동엄마까투리 25")
#win.attributes('-fullscreen', True) #fullscreen
win.configure(bg='gray')

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
    print("%dH %dM %dS" % (h,m,s))

        
