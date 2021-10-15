import turtle as t

def face(x, y):
    """画脸"""
    t.begin_fill()
    t.penup()
    # 将海龟移动到指定的坐标
    t.goto(x, y)
    t.pendown()
    # 设置海龟的方向
    t.setheading(40)

    t.circle(-150, 69)
    t.fillcolor("#FBD624")
    # 将海龟移动到指定的坐标

    t.penup()
    t.goto(53.14, 113.29)
    t.pendown()

    t.setheading(300)
    t.circle(-150, 30)
    t.setheading(295)
    t.circle(-140, 20)
    print(t.position())
    t.forward(5)
    t.setheading(260)
    t.circle(-80, 70)
    print(t.position())
    t.penup()
    t.goto(-74.43, -79.09)
    t.pendown()

    t.penup()
    # 将海龟移动到指定的坐标
    t.goto(-144, 103)
    t.pendown()
    t.setheading(242)
    t.circle(110, 35)
    t.right(10)
    t.forward(10)
    t.setheading(250)
    t.circle(80, 115)
    print(t.position())

    t.penup()
    t.goto(-74.43, -79.09)
    t.pendown()
    t.setheading(10)
    t.penup()
    t.goto(-144, 103)

    t.pendown()
    t.penup()
    t.goto(x, y)
    t.pendown()

    t.end_fill()

    # 下巴
    t.penup()
    t.goto(-50, -82.09)
    t.pendown()
    t.pencolor("#DDA120")
    t.fillcolor("#DDA120")
    t.begin_fill()
    t.setheading(-12)
    t.circle(120, 25)
    t.setheading(-145)
    t.forward(30)
    t.setheading(180)
    t.circle(-20, 20)
    t.setheading(143)
    t.forward(30)
    t.end_fill()
    # penup()
    # # 将海龟移动到指定的坐标
    # goto(0, 0)
    # pendown()


def eye():
    """画眼睛"""
    # 左眼
    t.color("black", "black")
    t.penup()
    t.goto(-110, 27)
    t.pendown()
    t.begin_fill()
    t.setheading(0)
    t.circle(24)
    t.end_fill()
    # 左眼仁
    t.color("white", "white")
    t.penup()
    t.goto(-105, 51)
    t.pendown()
    t.begin_fill()
    t.setheading(0)
    t.circle(10)
    t.end_fill()
    # 右眼
    t.color("black", "black")
    t.penup()
    t.goto(25, 40)
    t.pendown()
    t.begin_fill()
    t.setheading(0)
    t.circle(24)
    t.end_fill()
    # 右眼仁
    t.color("white", "white")
    t.penup()
    t.goto(17, 62)
    t.pendown()
    t.begin_fill()
    t.setheading(0)
    t.circle(10)
    t.end_fill()


def cheek():
    """画脸颊"""
    # 右边
    t.color("#9E4406", "#FE2C21")
    t.penup()
    t.goto(-130, -50)
    t.pendown()
    t.begin_fill()
    t.setheading(0)
    t.circle(27)
    t.end_fill()

    # 左边
    t.color("#9E4406", "#FE2C21")
    t.penup()
    t.goto(53, -20)
    t.pendown()
    t.begin_fill()
    t.setheading(0)
    t.circle(27)
    t.end_fill()


def nose():
    """画鼻子"""
    t.color("black", "black")
    t.penup()
    t.goto(-40, 38)
    t.pendown()
    t.begin_fill()
    t.circle(7, steps=3)
    t.end_fill()


def mouth():
    """画嘴"""
    t.color("black", "#F35590")
    # 嘴唇
    t.penup()
    t.goto(-10, 22)
    t.pendown()
    t.begin_fill()
    t.setheading(260)
    t.forward(60)
    t.circle(-11, 150)
    t.forward(55)
    print(t.position())
    t.penup()
    t.goto(-38.46, 21.97)
    t.pendown()
    t.end_fill()

    # 舌头
    t.color("#6A070D", "#6A070D")
    t.begin_fill()
    t.penup()
    t.goto(-10.00, 22.00)
    t.pendown()
    t.penup()
    t.goto(-14.29, -1.7)
    t.pendown()
    t.penup()
    t.goto(-52, -5)
    t.pendown()
    t.penup()
    t.goto(-60.40, 12.74)
    t.pendown()
    t.penup()
    t.goto(-38.46, 21.97)
    t.pendown()
    t.penup()
    t.goto(-10.00, 22.00)
    t.pendown()

    t.end_fill()

    t.color("black", "#FFD624")

    t.penup()
    t.goto(-78, 15)
    t.pendown()
    t.begin_fill()
    t.setheading(-25)
    for i in range(2):
        t.setheading(-25)
        t.circle(35, 70)

    t.end_fill()
    t.color("#AB1945", "#AB1945")
    t.penup()
    t.goto(-52, -5)
    t.pendown()
    t.begin_fill()
    t.setheading(40)
    t.circle(-33, 70)
    t.goto(-16, -1.7)
    t.penup()
    t.goto(-18, -17)
    t.pendown()
    t.setheading(155)
    t.circle(25, 70)
    t.end_fill()


def ear():
    """画耳朵"""
    # 左耳
    t.color("black", "#FFD624")
    t.penup()
    t.goto(-145, 93)
    t.pendown()
    t.begin_fill()
    t.setheading(165)
    t.circle(-248, 50)
    t.right(120)
    t.circle(-248, 50)
    t.end_fill()
    t.color("black", "black")
    t.penup()
    t.goto(-240, 143)
    t.pendown()
    t.begin_fill()
    t.setheading(107)
    t.circle(-170, 25)
    t.left(80)
    t.circle(229, 15)
    t.left(120)
    t.circle(300, 15)
    t.end_fill()

    # 右耳
    t.color("black", "#FFD624")
    t.penup()
    t.goto(30, 136)
    t.pendown()
    t.begin_fill()
    t.setheading(64)
    t.circle(-248, 50)

    t.right(120)
    t.circle(-248, 50)
    t.end_fill()
    t.color("black", "black")
    t.penup()
    t.goto(160, 200)
    t.pendown()
    t.begin_fill()
    t.setheading(52)
    t.circle(170, 25)
    t.left(116)
    t.circle(229, 15)
    t.left(71)
    t.circle(-300, 15)
    t.end_fill()

def setting():
  """设置参数"""
  t.pensize(2)
   # 隐藏海龟
  t.hideturtle()
  t.speed(10)


def main():
    """主函数"""
    setting()
    face(-132, 115)
    eye()
    cheek()
    nose()
    mouth()
    ear()
    t.done()


if __name__ == '__main__':
    main()
