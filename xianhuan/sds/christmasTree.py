#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""

import turtle as tur


# 爱心函数
# r为半圆半径，l = 2r为正方形边长
# 调整半径即可调整爱心大小
def loving_heart(r):
    l = 2 * r
    tur.left(45)
    tur.forward(l)
    tur.circle(r, 180)
    tur.right(90)
    tur.circle(r, 180)
    tur.forward(l)


# 树函数(递归)
def tree(d, s):
    if d <= 0:
        return
    tur.forward(s)
    tree(d - 1, s * .8)
    tur.right(120)
    tree(d - 3, s * .5)
    tur.right(120)
    tree(d - 3, s * .5)
    tur.right(120)
    # 回退函数
    tur.backward(s)


# 画爱心部分
tur.penup()
# 设置起点位置
tur.goto(0, 200)
tur.pendown()
# 设置画笔颜色
tur.pencolor('pink')
tur.color('pink')
# 对图形进行填充
tur.begin_fill()
# 执行画爱心函数
loving_heart(20)
tur.end_fill()

# 画树部分
n = 100
tur.speed('fastest')
tur.right(225)
tur.color("dark green")
tur.backward(n * 4.8)
tree(15, n)
tur.backward(n / 5)
tur.penup()
tur.Turtle().screen.delay(2)
tur.goto(80, 0)
tur.pendown()
tur.color("gold")
tur.write("Merry Christmas!", font=("Times", 32, "bold"))
tur.hideturtle()
