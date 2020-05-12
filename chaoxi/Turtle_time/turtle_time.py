import turtle as tl
import time
from datetime import datetime,timedelta


def drawGap(): #绘制数码管间隔
    #提起画笔
    tl.pu()
    # 数码管间隔
    tl.fd(9)

def drawLine(draw):   #绘制单段数码管
    drawGap()
    tl.pendown() \
        if draw else tl.penup()
    tl.fd(40)
    drawGap()
    tl.right(90)

def drawDigit(d): #根据数字绘制七段数码管
    # 每个数字由7段数码管组成
    drawLine(True) if d in [2, 3, 4, 5, 6, 8, 9] else drawLine(False)
    drawLine(True) if d in [0, 1, 3, 4, 5, 6, 7, 8, 9] else drawLine(False)
    drawLine(True) if d in [0, 2, 3, 5, 6, 8, 9] else drawLine(False)
    drawLine(True) if d in [0, 2, 6, 8] else drawLine(False)
    tl.left(90)
    #
    drawLine(True) if d in [0, 4, 5, 6, 8, 9] else drawLine(False)
    drawLine(True) if d in [0, 2, 3, 5, 6, 7, 8, 9] else drawLine(False)
    drawLine(True) if d in [0, 1, 2, 3, 4, 7, 8, 9] else drawLine(False)
    tl.left(180)
    tl.penup()
    tl.fd(20)

def drawDate(date):
    tl.pencolor("#AB82FF")
    for i in date: #根据设置的符号分隔年月日
        if i == '-':
            tl.write('年',font=("Arial", 22, "normal"))
            tl.pencolor("#B3EE3A")
            tl.fd(40)
        elif i == '=':
            tl.write('月',font=("Arial", 22, "normal"))
            tl.pencolor("#FFD700")
            tl.fd(40)
        elif i == '+':
            tl.write('日',font=("Arial", 22, "normal"))
        else:
            drawDigit(eval(i))
def all(day):
    tl.goto(-350,-300)
    tl.pencolor("SlateBlue")
    tl.write('总共',font=("Arial", 40, "normal"))
    tl.fd(110)
    for j in day:
        drawDigit(eval(j))
    tl.write('天',font=("Arial", 40, "normal"))

def count(t1, t2, t3):
    t = t1*365
    if t2 in [1, 2]:
        t += t2*30
    if t2 in [3]:
        t = t+91
    if t2 == 4:
        t += 122
    if t2 == 5:
        t += 152
    if t2 == 6:
        t += 183
    if t2 == 7:
        t += 213
    if t2 == 8:
        t += 244
    if t2 == 9:
        t += 275
    if t2 == 10:
        t += 303
    if t2 == 11:
        t += 334
    t += t3
    return(str(t))

#　画出日期
def turtle_date():
    tl.color('MediumTurquoise')
    tl.penup()
    tl.goto(-350,370)
    tl.pendown()
    # 获取到当前日期
    tl.write('今天是：',font=("Arial", 22, "normal"))
    tl.pensize(5)
    tl.penup()
    tl.goto(-350,300)
    tl.pendown()
    drawDate(time.strftime('%Y-%m=%d+',time.gmtime()))
    tl.color('MediumTurquoise')
    tl.penup()
    tl.goto(-350,190)
    tl.pensize(1)
    tl.pendown()
    tl.pencolor("MediumTurquoise")
    tl.write('我加入 Python 团队的时间是：',font=("Arial", 22, "normal"))
    tl.penup()
    tl.goto(-350,110)
    tl.pendown()
    tl.pensize(5)
    # 加入团队的时间
    drawDate('2019-09=03+')
    tl.penup()
    tl.goto(-350,0)
    tl.pensize(1)
    tl.pendown()
    tl.pencolor("MediumTurquoise")
    # 从加入日期到当前日期的月和天数
    tl.write('我和团队成员一起经历了：',font=("Arial", 22, "normal"))
    tl.penup()
    tl.goto(0,-100)
    tl.pensize(1)
    tl.pendown()

# 设置画笔
# def main():
#     tl.setup(800, 350, 200, 200) #设置画布窗口大小以及位置
#     tl.penup()
#     tl.fd(-350)
#     tl.pensize(5)
#     t = time.gmtime() #获取系统当前时间
#     print(t)
#     drawDate(time.strftime('%Y-%m=%d+', t))
#     tl.hideturtle()
#     tl.done()

def main():
    tl.setup(1000, 1000, 200, 200)
    turtle_date()
    tl.penup()
    tl.fd(-350)
    tl.pensize(5)
#    drawDate('2018-10=10+')
    t1 = time.gmtime()
    t2 = t1.tm_year-2019
    t3 = t1.tm_mon-9
    if t3<0:
        t2 -= 1
        t3 += 12
    t4 = t1.tm_mday-3
    if t4 < 0:
        t3 -= 1
        if t1.tm_mon-1 in [1, 3, 5, 7, 8, 10, 12]:
            t4 += 31
        else:
            t4+=30
    tatol = count(t2,t3,t4)
    drawDate(str(t2)+'-'+str(t3)+'='+str(t4)+'+')
    all(tatol)

    # 隐藏画笔
    tl.hideturtle()

    # 落笔
    tl.done()


if __name__ == '__main__':
    main()



