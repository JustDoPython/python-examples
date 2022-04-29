import turtle as t
from turtle import *

angle = 60  # 通过改变角度，绘制出各种多边形
t.bgcolor('black')
t.pensize(2)
randomColor = ['red', 'blue', 'green', 'purple', 'gold', 'pink']
t.speed(0)
for i in range(200):
    t.color(randomColor[i % 6])
    t.circle(i)
    t.rt(angle + 1)
up()
color("#0fe6ca")
goto(0, 0)
down()
