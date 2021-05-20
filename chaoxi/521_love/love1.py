import turtle
import time

def hart_arc():
    for i in range(200):
        turtle.right(1)
        turtle.forward(2)


def move_pen_position(x, y):
    turtle.hideturtle()  # 隐藏画笔（先）
    turtle.up()  # 提笔
    turtle.goto(x, y)  # 移动画笔到指定起始坐标（窗口中心为0,0）
    turtle.down()  # 下笔
    turtle.showturtle()  # 显示画笔


love = input("请输入表白话语：")
signature = input("请签署你的名字:")
date=input("请写上日期：")

if love == '':
    love = 'I Love You'

turtle.setup(width=800, height=500)  # 窗口（画布）大小
turtle.color('red', 'pink')  # 画笔颜色
turtle.pensize(3)  # 画笔粗细
turtle.speed(1)  # 描绘速度
# 初始化画笔起始坐标
move_pen_position(x=0, y=-180)  # 移动画笔位置
turtle.left(140)  # 向左旋转140度

turtle.begin_fill()  # 标记背景填充位置

# 画图和展示
turtle.forward(224)  # 向前移动画笔，长度为224
# 画爱心圆弧
hart_arc()  # 左侧圆弧
turtle.left(120)  # 调整画笔角度
hart_arc()  # 右侧圆弧
# 画心形直线（ 右下方 ）
turtle.forward(224)

turtle.end_fill()  # 标记背景填充结束位置

move_pen_position(x=70, y=160)  # 移动画笔位置
turtle.left(185)  # 向左旋转180度
turtle.circle(-110,185)  # 右侧圆弧
# 画心形直线（ 右下方 ）
#turtle.left(20)  # 向左旋转180度
turtle.forward(50)
move_pen_position(x=-180, y=-180)  # 移动画笔位置
turtle.left(180)  # 向左旋转140度

# 画心形直线（ 左下方 ）
turtle.forward(600)  # 向前移动画笔，长度为224

# 在心形中写上表白话语
move_pen_position(0,50)  # 表白语位置
turtle.hideturtle()  # 隐藏画笔
turtle.color('#CD5C5C', 'pink')  # 字体颜色
# font:设定字体、尺寸（电脑下存在的字体都可设置）  align:中心对齐
turtle.write(love, font=('Arial', 20, 'bold'), align="center")

# 签写署名和日期
if (signature != '') & (date != ''):
    turtle.color('red', 'pink')
    time.sleep(2)
    move_pen_position(220, -180)
    turtle.hideturtle()  # 隐藏画笔
    turtle.write(signature, font=('Arial', 20), align="center")
    move_pen_position(220, -220)
    turtle.hideturtle()  # 隐藏画笔
    turtle.write(date, font=('Arial', 20), align="center")

#点击窗口关闭程序
window = turtle.Screen()
window.exitonclick()

