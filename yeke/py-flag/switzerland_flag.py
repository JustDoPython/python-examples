import turtle

def draw_crossshaped(aTurtle, width=0, height=0, color=None):
    aTurtle = turtle.Turtle()
    aTurtle.hideturtle()
    aTurtle.penup()
    aTurtle.goto(30, 50)
    aTurtle.begin_fill()
    aTurtle.fillcolor(color)
    for i in range(4):
        aTurtle.pendown()
        aTurtle.fd(width)
        aTurtle.rt(90)
        aTurtle.fd(height)
        aTurtle.rt(90)
        aTurtle.fd(width)
        aTurtle.lt(90)
    aTurtle.end_fill()

def draw_RQ(times=20.0):
    width, height = 26 * times, 26 * times
    window = turtle.Screen()
    aTurtle = turtle.Turtle()
    aTurtle.hideturtle()
    aTurtle.speed(10)
    aTurtle.penup()
    aTurtle.goto(-width / 2, height / 2)
    aTurtle.pendown()
    aTurtle.begin_fill()
    aTurtle.fillcolor('red')
    aTurtle.fd(width)
    aTurtle.right(90)
    aTurtle.fd(height)
    aTurtle.right(90)
    aTurtle.fd(width)
    aTurtle.right(90)
    aTurtle.fd(height)
    aTurtle.right(90)
    aTurtle.end_fill()
    draw_crossshaped(aTurtle, width=80, height=80, color='white')
    window.exitonclick()

if __name__ == '__main__':
    draw_RQ()
