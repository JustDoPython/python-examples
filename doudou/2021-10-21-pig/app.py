import turtle as t


def nose(x, y):  # 鼻子
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.setheading(-30)
    t.begin_fill()
    a = 0.4
    for i in range(120):
        if 0 <= i < 30 or 60 <= i < 90:
            a = a + 0.08
            t.left(3)
            t.forward(a)
        else:
            a = a - 0.08
            t.left(3)
            t.forward(a)
    t.end_fill()

    t.penup()
    t.setheading(90)
    t.forward(25)
    t.setheading(0)
    t.forward(10)
    t.pendown()
    t.pencolor(255, 155, 192)
    t.setheading(10)
    t.begin_fill()
    t.circle(5)
    t.color(160, 82, 45)
    t.end_fill()

    t.penup()
    t.setheading(0)
    t.forward(20)
    t.pendown()
    t.pencolor(255, 155, 192)
    t.setheading(10)
    t.begin_fill()
    t.circle(5)
    t.color(160, 82, 45)
    t.end_fill()


def head(x, y):  # 头
    t.color((255, 155, 192), "pink")
    t.penup()
    t.goto(x, y)
    t.setheading(0)
    t.pendown()
    t.begin_fill()
    t.setheading(180)
    t.circle(300, -30)
    t.circle(100, -60)
    t.circle(80, -100)
    t.circle(150, -20)
    t.circle(60, -95)
    t.setheading(161)
    t.circle(-300, 15)
    t.penup()
    t.goto(-100, 100)
    t.pendown()
    t.setheading(-30)
    a = 0.4
    for i in range(60):
        if 0 <= i < 30 or 60 <= i < 90:
            a = a + 0.08
            t.lt(3)
            t.fd(a)
        else:
            a = a - 0.08
            t.lt(3)
            t.fd(a)
    t.end_fill()


def ears(x, y):  # 耳朵
    t.color((255, 155, 192), "pink")
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.begin_fill()
    t.setheading(100)
    t.circle(-50, 50)
    t.circle(-10, 120)
    t.circle(-50, 54)
    t.end_fill()

    t.penup()
    t.setheading(90)
    t.forward(-12)
    t.setheading(0)
    t.forward(30)
    t.pendown()
    t.begin_fill()
    t.setheading(100)
    t.circle(-50, 50)
    t.circle(-10, 120)
    t.circle(-50, 56)
    t.end_fill()


def eyes(x, y):  # 眼睛
    t.color((255, 155, 192), "white")
    t.penup()
    t.setheading(90)
    t.forward(-20)
    t.setheading(0)
    t.forward(-95)
    t.pendown()
    t.begin_fill()
    t.circle(15)
    t.end_fill()

    t.color("black")
    t.penup()
    t.setheading(90)
    t.forward(12)
    t.setheading(0)
    t.forward(-3)
    t.pendown()
    t.begin_fill()
    t.circle(3)
    t.end_fill()

    t.color((255, 155, 192), "white")
    t.penup()
    t.seth(90)
    t.forward(-25)
    t.seth(0)
    t.forward(40)
    t.pendown()
    t.begin_fill()
    t.circle(15)
    t.end_fill()

    t.color("black")
    t.penup()
    t.setheading(90)
    t.forward(12)
    t.setheading(0)
    t.forward(-3)
    t.pendown()
    t.begin_fill()
    t.circle(3)
    t.end_fill()


def cheek(x, y):  # 腮
    t.color((255, 155, 192))
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.setheading(0)
    t.begin_fill()
    t.circle(30)
    t.end_fill()


def mouth(x, y):  # 嘴
    t.color(239, 69, 19)
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.setheading(-80)
    t.circle(30, 40)
    t.circle(40, 80)


def body(x, y):  # 身体
    t.color("red", (255, 99, 71))
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.begin_fill()
    t.setheading(-130)
    t.circle(100, 10)
    t.circle(300, 30)
    t.setheading(0)
    t.forward(230)
    t.setheading(90)
    t.circle(300, 30)
    t.circle(100, 3)
    t.color((255, 155, 192), (255, 100, 100))
    t.setheading(-135)
    t.circle(-80, 63)
    t.circle(-150, 24)
    t.end_fill()


def hands(x, y):  # 手
    t.color((255, 155, 192))
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.setheading(-160)
    t.circle(300, 15)
    t.penup()
    t.setheading(90)
    t.forward(15)
    t.setheading(0)
    t.forward(0)
    t.pendown()
    t.setheading(-10)
    t.circle(-20, 90)

    t.penup()
    t.setheading(90)
    t.forward(30)
    t.setheading(0)
    t.forward(237)
    t.pendown()
    t.setheading(-20)
    t.circle(-300, 15)
    t.penup()
    t.setheading(90)
    t.forward(20)
    t.setheading(0)
    t.forward(0)
    t.pendown()
    t.setheading(-170)
    t.circle(20, 90)


def foot(x, y):  # 脚
    t.pensize(10)
    t.color((240, 128, 128))
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.setheading(-90)
    t.forward(40)
    t.setheading(-180)
    t.color("black")
    t.pensize(15)
    t.fd(20)

    t.pensize(10)
    t.color((240, 128, 128))
    t.penup()
    t.setheading(90)
    t.forward(40)
    t.setheading(0)
    t.forward(90)
    t.pendown()
    t.setheading(-90)
    t.forward(40)
    t.setheading(-180)
    t.color("black")
    t.pensize(15)
    t.fd(20)


def tail(x, y):  # 尾巴
    t.pensize(4)
    t.color((255, 155, 192))
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.seth(0)
    t.circle(70, 20)
    t.circle(10, 330)
    t.circle(70, 30)


def setting():  # 参数设置
    t.pensize(4)
    t.hideturtle()
    t.colormode(255)
    t.color((255, 155, 192), "pink")
    t.setup(840, 500)
    t.speed(10)


def main():
    setting()  # 设置
    nose(-100, 100)  # 鼻子
    head(-69, 167)  # 头
    ears(0, 160)  # 耳朵
    eyes(0, 140)  # 眼睛
    cheek(80, 10)  # 腮
    mouth(-20, 30)  # 嘴
    body(-32, -8)  # 身体
    hands(-56, -45)  # 手
    foot(2, -177)  # 脚
    tail(148, -155)  # 尾巴
    t.done()


if __name__ == '__main__':
    main()
