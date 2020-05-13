import turtle as tl
import time


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
    tl.left(200)
    tl.penup()
    tl.fd(20)
    tl.hideturtle()
    tl.done()

def drawDate(date):
    tl.pencolor("#AB82FF")
    for i in date: #根据设置的符号分隔年月日
        if i == '-':
            tl.write('年',font=("Arial", 18, "normal"))
            tl.pencolor("#B3EE3A")
            tl.fd(40)
        elif i == '=':
            tl.write('月',font=("Arial", 18, "normal"))
            tl.pencolor("#FFD700")
            tl.fd(40)
        elif i == '+':
            tl.write('日',font=("Arial", 18, "normal"))
        else:
            drawDigit(eval(i))

if __name__ == '__main__':
    drawDigit(8)

