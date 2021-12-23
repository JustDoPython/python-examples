#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""

import turtle as t
from turtle import *
import random as r


n = 100.0

speed(10000)  # 定义速度
pensize(5)  # 画笔宽度
screensize(800, 800, bg='black')  # 定义背景颜色，可以自己换颜色
left(90)
forward(250)              # 开始的高度
color("orange", "yellow")  # 定义最上端星星的颜色，外圈是orange，内部是yellow
begin_fill()
left(126)


# 画五角星
for i in range(5):
    forward(n / 5)
    right(144)  # 五角星的角度
    forward(n / 5)
    left(72)  # 继续换角度
end_fill()
right(126)


# 定义画彩灯的方法
def drawlight():
    if r.randint(0, 50) == 0:  # 如果觉得彩灯太多，可以把取值范围加大一些，对应的灯就会少一些
        color('tomato')  # 定义第一种颜色
        circle(3)  # 定义彩灯大小
    elif r.randint(0, 30) == 1:
        color('orange')  # 定义第二种颜色
        circle(4)  # 定义彩灯大小
    elif r.randint(0, 50) == 2:
        color('blue')  # 定义第三种颜色
        circle(2)  # 定义彩灯大小
    elif r.randint(0, 30) == 3:
        color('white')  # 定义第四种颜色
        circle(4)  # 定义彩灯大小
    else:
        color('dark green')  # 其余的随机数情况下画空的树枝


color("dark green")  # 定义树枝的颜色
backward(n * 4.8)

# 画树
def tree(d, s):
    speed(100)
    if d <= 0: return
    forward(s)
    tree(d - 1, s * .8)
    right(120)
    tree(d - 3, s * .5)
    drawlight()  # 同时调用小彩灯的方法
    right(120)
    tree(d - 3, s * .5)
    right(120)
    backward(s)


tree(15, 100)
backward(50)


# 循环画最底端的小装饰
for i in range(200):
    a = 200 - 400 * r.random()
    b = 10 - 20 * r.random()
    up()
    forward(b)
    left(90)
    forward(a)
    down()
    if r.randint(0, 1) == 0:
        color('tomato')
    else:
        color('wheat')
    circle(2)
    up()
    backward(a)
    right(90)
    backward(b)


# 画雪人 (n,m)是头和身子交点的坐标，a是头的大小，m是身体的大小
def drawsnowman(n,m,a,b):
    speed(100)
    t.goto(n, m)
    t.pencolor("white")
    t.pensize(2)
    t.fillcolor("white")
    t.seth(0)
    t.begin_fill()
    t.circle(a)
    t.end_fill()
    t.seth(180)
    t.begin_fill()
    t.circle(b)
    t.end_fill()
    t.pencolor("black")
    t.fillcolor("black")
    t.penup()    # 右眼睛
    t.goto(n-a/4, m+a)
    t.seth(0)
    t.pendown()
    t.begin_fill()
    t.circle(2)
    t.end_fill()
    t.penup()    # 左眼睛
    t.goto(n+a/4, m+a)
    t.seth(0)
    t.pendown()
    t.begin_fill()
    t.circle(2)
    t.end_fill()
    t.penup()  # 画嘴巴
    t.goto(n, m+a/2)
    t.seth(0)
    t.pendown()
    t.fd(5)
    t.penup()       # 画扣子
    t.pencolor("red")
    t.fillcolor("red")
    t.goto(n, m-b/4)
    t.pendown()
    t.begin_fill()
    t.circle(2)
    t.end_fill()
    t.penup()
    t.pencolor("yellow")
    t.fillcolor("yellow")
    t.goto(n, m-b/2)
    t.pendown()
    t.begin_fill()
    t.circle(2)
    t.end_fill()
    t.penup()
    t.pencolor("orange")
    t.fillcolor("orange")
    t.goto(n, m-(3*b)/4)
    t.pendown()
    t.begin_fill()
    t.circle(2)
    t.end_fill()

drawsnowman(-200, -200, 20, 30)
drawsnowman(-250, -200, 30, 40)

t.up()
t.goto(100, 200)
t.down()
t.color("dark red", "red")  # 定义字体颜色
t.penup()
t.write("Merry Christmas, My Love!", font=("Comic Sans MS", 16, "bold"))  # 定义文字、位置、字体、大小
t.end_fill()


# 画雪花
def drawsnow():
    t.ht()  # 隐藏笔头，ht=hideturtle
    t.pensize(2)  # 定义笔头大小
    for i in range(200):  # 画多少雪花
        t.pencolor("white")  # 定义画笔颜色为白色，其实就是雪花为白色
        t.pu()  # 提笔，pu=penup
        t.setx(r.randint(-350, 350))  # 定义x坐标，随机从-350到350之间选择
        t.sety(r.randint(-100, 350))  # 定义y坐标，注意雪花一般在地上不会落下，所以不会从太小的纵座轴开始
        t.pd()  # 落笔，pd=pendown
        dens = 6  # 雪花瓣数设为6
        snowsize = r.randint(1, 10)  # 定义雪花大小
        for j in range(dens):  # 就是6，那就是画5次，也就是一个雪花五角星
            # t.forward(int(snowsize))  #int（）取整数
            t.fd(int(snowsize))
            t.backward(int(snowsize))
            # t.bd(int(snowsize))  #注意没有bd=backward，但有fd=forward，小bug
            t.right(int(360 / dens))  # 转动角度


drawsnow()  # 调用画雪花的方法
t.done()  # 完成,否则会直接关闭


