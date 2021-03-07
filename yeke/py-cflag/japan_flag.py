import turtle

turtle.setup(width=600, height=400)
# 设置画笔起点
turtle.penup()
turtle.goto(0, -50)
turtle.pendown()
# 设置画笔属性
turtle.pensize(5)
turtle.pencolor("red")
turtle.fillcolor("red")
# 绘制速度
turtle.speed(10)
turtle.begin_fill()
turtle.circle(50)
turtle.end_fill()
turtle.hideturtle()
turtle.mainloop()