import turtle as t
import time
'''
部分函数及参数说明:
pen_move():画每个部位时，都必须先抬起画笔，移动到指定位置后落下
pen_set():用来设置画笔的颜色尺寸等
t.setup(width,height):入宽和高为整数时,表示像素;为小数时,表示占据电脑屏幕的比例
t.speed()：设置画笔速度
t.goto():以左下角为坐标原点，进行画笔的移动
t.circle(radius，extent):设置指定半径radius的圆，参数为半径，半径为正(负)，表示圆心在画笔的左边(右边)画圆，extent为角度，若画圆则无须添加。如：t.circle(-20,90),顺时针，半径20画弧，弧度90
t.seth(degree)绝对角度，将画笔的方向设置为一定的度数方向，0-东；90-北；180-西；270-南
'''

wight=800
height=600
t.setup(wight,height)
t.speed(10)

def pen_move(x,y):
    t.penup()
    t.goto(x-wight/2+50,y-height/2+50)
    t.pendown()

def pen_set(size,color):
    t.pensize(size)
    t.color(color)

def draw():
    #第一个眼睛
    pen_move(300,350)
    pen_set(2,'black')
    t.begin_fill()
    t.circle(10)
    t.end_fill()
    # 第一个眼眶
    pen_move(300,350)
    t.circle(15)
    #第二个眼睛
    pen_move(400,350)
    t.begin_fill()
    t.circle(10)
    t.end_fill()
    # 第二个眼眶
    pen_move(400,350)
    t.circle(15)

    # 嘴
    pen_move(340,300)
    t.seth(0)
    t.left(45)
    t.forward(30)
    pen_move(360, 300)
    t.seth(180)
    t.left(45+270)
    t.forward(30)

    # 右边脸框
    t.seth(0)
    pen_move(340,260)
    t.circle(90,150)

    # 左边脸框
    t.seth(180)
    pen_move(340,260)
    t.circle(-90,140)
    # time.sleep(100)

    #耳朵
    # t.seth(0)
    pen_move(260, 400)
    t.left(100)
    # t.forward(100)
    t.circle(-60,70)

    #合上耳朵
    pen_move(285, 430)
    t.left(40)
    t.circle(60,50)

    #右耳朵
    pen_move(380,430)
    t.right(90)
    t.circle(-60,50)

    pen_move(413,410)
    t.left(30)
    t.circle(60,60)

    # 左边身子的线条
    pen_move(320, 270)
    t.seth(180)
    t.left(70)
    t.forward(260)

    # 身子底部线条
    pen_move(230, 30)
    t.seth(0)
    # t.left(60)
    t.forward(240)

    # 右边身子线条
    pen_move(380, 270)
    # t.seth(0)
    t.right(70)
    t.forward(260)

    # 尾巴
    pen_move(380+90, 270-240)
    t.left(60)
    pen_set(6,'black')
    t.circle(130,100)

    t.left(10)
    t.circle(160,40)
    t.left(20)
    t.circle(100,30)
    t.left(50)
    t.circle(80,50)
    t.left(70)
    t.circle(70,40)
    t.left(70)
    t.circle(60,30)
    t.left(70)
    t.circle(60,20)
    t.left(60)
    t.circle(60,10)
    t.left(60)
    t.circle(10,5)
    time.sleep(1)

draw()