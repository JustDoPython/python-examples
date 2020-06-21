#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
import turtle
from datetime import *

# 抬起画笔，向前运动一段距离放下
def skip(step):
    turtle.penup()
    turtle.forward(step)
    turtle.pendown()

def mkHand(name, length):
    # 注册Turtle形状，建立表针Turtle
    turtle.reset()
    # 先反向运动一段距离，终点作为绘制指针的起点
    skip(-length * 0.1)
    # 开始记录多边形的顶点。当前的乌龟位置是多边形的第一个顶点。
    turtle.begin_poly()
    turtle.forward(length * 1.1)
    # 停止记录多边形的顶点。当前的乌龟位置是多边形的最后一个顶点。将与第一个顶点相连。
    turtle.end_poly()
    # 返回最后记录的多边形。
    handForm = turtle.get_poly()
    turtle.register_shape(name, handForm)

def init():
    global secHand, minHand, houHand, printer
    # 重置Turtle指向北
    turtle.mode("logo")
    # 建立三个表针Turtle并初始化
    mkHand("secHand", 135)
    mkHand("minHand", 125)
    mkHand("houHand", 90)
    secHand = turtle.Turtle()
    secHand.shape("secHand")
    minHand = turtle.Turtle()
    minHand.shape("minHand")
    houHand = turtle.Turtle()
    houHand.shape("houHand")

    for hand in secHand, minHand, houHand:
        hand.shapesize(1, 1, 3)
        hand.speed(0)

    # 建立输出文字Turtle
    printer = turtle.Turtle()
    # 隐藏画笔的turtle形状
    printer.hideturtle()
    printer.penup()

# 绘制表盘
def setupClock(radius):
    # 建立表的外框
    turtle.reset()
    turtle.pensize(7)
    for i in range(60):
        # 向前移动半径值
        skip(radius)
        if i % 5 == 0:
            # 画长刻度线
            turtle.forward(20)
            # 回到中心点
            skip(-radius - 20)

            # 移动到刻度线终点
            skip(radius + 20)
            # 下面是写表盘刻度值,为了不与划线重叠，所以对于特殊位置做了处理
            if i == 0:
                turtle.write(int(12), align="center", font=("Courier", 14, "bold"))
            elif i == 30:
                skip(25)
                turtle.write(int(i/5), align="center", font=("Courier", 14, "bold"))
                skip(-25)
            elif (i == 25 or i == 35):
                skip(20)
                turtle.write(int(i/5), align="center", font=("Courier", 14, "bold"))
                skip(-20)
            else:
                turtle.write(int(i/5), align="center", font=("Courier", 14, "bold"))
            
            # 回到中心点
            skip(-radius - 20)
        else:
            # 画圆点
            turtle.dot(5)
            skip(-radius)
        # 顺时针移动6°
        turtle.right(6)

def week(t):
    week = ["星期一", "星期二", "星期三",
            "星期四", "星期五", "星期六", "星期日"]
    return week[t.weekday()]

def date(t):
    y = t.year
    m = t.month
    d = t.day
    return "%s %d%d" % (y, m, d)

def tick():
    # 绘制表针的动态显示
    t = datetime.today()
    second = t.second + t.microsecond * 0.000001
    minute = t.minute + second / 60.0
    hour = t.hour + minute / 60.0
    secHand.setheading(6 * second)
    minHand.setheading(6 * minute)
    houHand.setheading(30 * hour)

    turtle.tracer(False)
    printer.forward(65)
    printer.write(week(t), align="center",
                  font=("Courier", 14, "bold"))
    printer.back(130)
    printer.write(date(t), align="center",
                  font=("Courier", 14, "bold"))
    printer.home()
    turtle.tracer(True)

    # 100ms后继续调用tick
    turtle.ontimer(tick, 100)

def main():
    # 打开/关闭龟动画，并为更新图纸设置延迟。
    turtle.tracer(False)
    init()
    setupClock(160)
    turtle.tracer(True)
    tick()
    turtle.mainloop()

if __name__ == "__main__":
    main()