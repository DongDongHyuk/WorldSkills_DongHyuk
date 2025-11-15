import turtle as t
import random as r
a = 30; b = 10
t.speed(0)
t.bgcolor("black")
t.pensize(3)
t.color("yellow")
while True:
    t.up()
    t.forward(30 + b)
    t.down()
    t.forward(-a)
    t.lt(-30)
    t.forward(a)
    t.lt(150)
    t.forward(a)
    t.lt(150)
    t.forward(a)
    t.lt(135)
    t.forward(27.6)
    b += 3
