import turtle as t

t.speed(5)
t.pensize(1)
t.screensize(500, 500)
t.bgcolor('white')

head_color = '#029FEC'
scarf_color = '#E20030'
nose_color = '#EB0134'
bell_color = '#FEE241'
color_white = '#FFFFFF'


def go_to(x=0, y=0):
    t.up()
    t.goto(x, y)
    t.down()


# 头部
def head():
    t.up()
    t.circle(150, 45)
    t.down()
    t.fillcolor(head_color)
    t.begin_fill()
    t.circle(150, 270)
    t.end_fill()


# 围巾
def scarf():
    t.fillcolor(scarf_color)
    t.begin_fill()
    t.seth(0)
    t.fd(216)
    t.circle(-5, 90)
    t.fd(10)
    t.circle(-5, 90)
    t.fd(220)
    t.circle(-5, 90)
    t.fd(10)
    t.circle(-5, 90)
    t.end_fill()


def face():
    t.fd(186)
    t.lt(45)
    t.fillcolor(color_white)
    t.begin_fill()
    t.circle(120, 100)
    t.seth(180)
    t.fd(120)
    t.seth(215)
    t.circle(120, 100)
    t.end_fill()


def draw_eyes():
    t.fillcolor(color_white)
    t.begin_fill()
    a = 2.5
    for i in range(120):
        if 0 <= i < 30 or 60 <= i < 90:
            a -= 0.05
        else:
            a += 0.05
        t.lt(3)
        t.fd(a)
    t.end_fill()


# 鼻子
def nose():
    go_to(-13, 166)
    t.seth(315)
    t.fillcolor(nose_color)
    t.begin_fill()
    t.circle(20)
    t.end_fill()


# 嘴巴
def mouth():
    go_to(0, 156)
    t.seth(270)
    t.fd(100)
    pos = t.pos()
    t.seth(0)
    t.circle(110, 60)
    go_to(pos[0], pos[1])
    t.seth(180)
    t.circle(-110, 60)


# 胡须
def mustache():
    h = 70
    go_to(30, 140)
    t.seth(15)
    t.fd(h)

    go_to(30, 130)
    t.seth(0)
    t.fd(h)

    go_to(30, 120)
    t.seth(-15)
    t.fd(h)

    go_to(-30, 140)
    t.seth(150)
    t.fd(h)

    go_to(-30, 130)
    t.seth(180)
    t.fd(h)

    go_to(-30, 120)
    t.seth(195)
    t.fd(h)


def eyes():
    go_to(0, 227)
    t.seth(90)
    draw_eyes()
    go_to(0, 227)
    t.seth(270)
    draw_eyes()


def fill_eyes():
    # 填充眼睛
    go_to(-15, 220)
    t.pensize(12)
    t.color('black')
    for i in range(30):
        t.forward(2)
        t.right(12)
    go_to(15, 220)
    for i in range(30):
        t.forward(2)
        t.left(12)
    t.pensize(1)


# 铃铛
def bell():
    # 大圆
    go_to(0, 33)
    t.pensize(1)
    t.fillcolor("#FCE341")
    t.begin_fill()
    t.circle(25)
    t.end_fill()

    # 横条纹
    go_to(-15, 22)
    t.seth(0)
    t.forward(42)
    go_to(-18, 17)
    t.seth(0)
    t.forward(47)

    # 小圆
    go_to(5, 0)
    t.pensize(1)
    t.color("black", '#79675d')
    t.begin_fill()
    t.circle(5)
    t.end_fill()
    t.seth(270)
    t.pensize(1)
    t.forward(15)


if __name__ == '__main__':
    head()
    scarf()
    face()
    eyes()
    fill_eyes()
    nose()
    mouth()
    mustache()
    bell()
    go_to()
    t.hideturtle()
    t.done()
