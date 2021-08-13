import turtle
import time
from turtle import mainloop, hideturtle


def clear_all():
    turtle.penup()
    turtle.goto(0, 0)
    turtle.color('white')
    turtle.pensize(800)
    turtle.pendown()
    turtle.setheading(0)
    turtle.fd(300)
    turtle.bk(600)


# 重定位海龟的位置
def go_to(x, y, state):
    turtle.pendown() if state else turtle.penup()
    turtle.goto(x, y)


def draw_heart(size):
    turtle.color('red', 'pink')
    turtle.pensize(2)
    turtle.pendown()
    turtle.setheading(150)
    turtle.begin_fill()
    turtle.fd(size)
    turtle.circle(size * -3.745, 45)
    turtle.circle(size * -1.431, 165)
    turtle.left(120)
    turtle.circle(size * -1.431, 165)
    turtle.circle(size * -3.745, 45)
    turtle.fd(size)
    turtle.end_fill()


# 画出发射爱心的小人
def draw_people(x, y):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.pensize(2)
    turtle.color('black')
    turtle.setheading(0)
    turtle.circle(60, 360)
    turtle.penup()
    turtle.setheading(90)
    turtle.fd(75)
    turtle.setheading(180)
    turtle.fd(20)
    turtle.pensize(4)
    turtle.pendown()
    turtle.circle(2, 360)
    turtle.setheading(0)
    turtle.penup()
    turtle.fd(40)
    turtle.pensize(4)
    turtle.pendown()
    turtle.circle(-2, 360)
    turtle.penup()
    turtle.goto(x, y)
    turtle.setheading(-90)
    turtle.pendown()
    turtle.fd(20)
    turtle.setheading(0)
    turtle.fd(35)
    turtle.setheading(60)
    turtle.fd(10)
    turtle.penup()
    turtle.goto(x, y)
    turtle.setheading(-90)
    turtle.pendown()
    turtle.fd(40)
    turtle.setheading(0)
    turtle.fd(35)
    turtle.setheading(-60)
    turtle.fd(10)
    turtle.penup()
    turtle.goto(x, y)
    turtle.setheading(-90)
    turtle.pendown()
    turtle.fd(60)
    turtle.setheading(-135)
    turtle.fd(60)
    turtle.bk(60)
    turtle.setheading(-45)
    turtle.fd(30)
    turtle.setheading(-135)
    turtle.fd(35)
    turtle.penup()


# 绘制文字
def draw_text(text, t_color, font_size, show_time):
    turtle.penup()
    turtle.goto(-350, 0)
    turtle.color(t_color)
    turtle.write(text, font=('宋体', font_size, 'normal'))
    time.sleep(show_time)
    clear_all()


# 爱心发射
def draw_():
    turtle.speed(0)
    draw_people(-250, 20)
    turtle.penup()
    turtle.goto(-150, -30)
    draw_heart(14)
    turtle.penup()
    turtle.goto(-200, -200)
    turtle.color('pink')
    turtle.write('Biu~', font=('宋体', 60, 'normal'))
    turtle.penup()
    turtle.goto(-20, -60)
    draw_heart(25)
    turtle.penup()
    turtle.goto(-70, -200)
    turtle.color('pink')
    turtle.write('Biu~', font=('宋体', 60, 'normal'))
    turtle.penup()
    turtle.goto(200, -100)
    draw_heart(45)
    turtle.penup()
    turtle.goto(150, -200)
    turtle.color('pink')
    turtle.write('Biu~', font=('宋体', 60, 'normal'))
    turtle.hideturtle()
    time.sleep(3)


def main():
    # 隐藏海龟
    hideturtle()
    turtle.setup(900, 500)

    draw_text("Are You Readly？", "black", 60, 0)
    draw_text("接下来", "skyblue", 60, 0)
    draw_text("感谢你的出现，让我的日子这么甜！", "pink", 35, 3)
    draw_()

    # 使用mainloop防止窗口卡死

    mainloop()

if __name__ == '__main__':

    main()