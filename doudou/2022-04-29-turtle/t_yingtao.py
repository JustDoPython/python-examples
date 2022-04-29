import turtle

toplevel = 8  # 一共递归6层
angle = 30
rangle = 15


def drawTree(length, level):
    turtle.left(angle)  # 绘制左枝
    turtle.color("black")
    turtle.forward(length)

    if level == toplevel:  # 叶子
        turtle.color("pink")
        turtle.circle(2, 360)

    if level < toplevel:  # 在左枝退回去之前递归
        drawTree(length - 10, level + 1)
    turtle.back(length)

    turtle.right(angle + rangle)  # 绘制右枝
    turtle.color("black")
    turtle.forward(length)

    if level == toplevel:  # 叶子
        turtle.color("pink")
        turtle.circle(2, 360)

    if level < toplevel:  # 在右枝退回去之前递归
        drawTree(length - 10, level + 1)
        turtle.color("black")
    turtle.back(length)
    turtle.left(rangle)


turtle.left(90)
turtle.penup()
turtle.back(300)
turtle.pendown()
turtle.forward(100)
turtle.speed(500)
drawTree(80, 1)

turtle.done()
