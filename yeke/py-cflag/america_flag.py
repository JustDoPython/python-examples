import turtle

# 画条纹
def drawSquar():
    turtle.color('black', 'red')
    turtle.begin_fill()
    for i in range(7):
        turtle.forward(600)
        turtle.left(90)
        turtle.forward(350 / 13)
        turtle.left(90)
        turtle.forward(600)
        turtle.right(90)
        turtle.forward(350 / 13)
        turtle.right(90)
    turtle.end_fill()
# 画左上角的小矩形
def drawSmallsqure():
    turtle.color('blue')
    turtle.begin_fill()
    turtle.left(90)
    turtle.forward(350 / 2)
    turtle.left(90)
    turtle.forward(300)
    turtle.left(90)
    turtle.forward(350 * 7 / 13)
    turtle.left(90)
    turtle.forward(300)
    turtle.end_fill()
# 画左上角的星星
def drawSrarts():
    x = -10
    y = 0
    for k in range(4):
        x = -15
        for i in range(6):
            turtle.goto(x, y)
            turtle.color('white')
            turtle.begin_fill()
            for j in range(5):
                turtle.left(144)
                turtle.forward(20)
            x -= 50
            turtle.end_fill()
        y += 350 / 13 * 2
    x = -10
    y = 350 / 13
    for i in range(3):
        x = -35
        for j in range(5):
            turtle.goto(x, y)
            turtle.color('white')
            turtle.begin_fill()
            for k in range(5):
                turtle.left(144)
                turtle.forward(20)
            x -= 50
            turtle.end_fill()
        y += 350 / 13 * 2
turtle.setup(0.8, 0.8, -100, -100)
turtle.speed(10)
turtle.pu()
turtle.forward(300)
turtle.left(90)
turtle.forward(350 / 2)
turtle.left(90)
drawSquar()
turtle.home()
drawSmallsqure()
turtle.home()
drawSrarts()
turtle.hideturtle()
turtle.done()