from turtle import Turtle

def line(t):
    t.backward(100)

def drawSpiral(myTurtle, lineLen):
    if lineLen < 500:
        myTurtle.forward(lineLen)
        myTurtle.right(90)
        drawSpiral(myTurtle, lineLen+20)

def fractalTree1(branchLen, t):
    t.forward(branchLen)
    if branchLen > 5:
        t.right(20)
        fractalTree1(branchLen - 15, t)
        t.left(20)
    t.backward(branchLen)
    if branchLen > 5:
        t.left(20)
        fractalTree1(branchLen - 15, t)
        t.right(20)
    # t.backward(branchLen)
def fractalTree2(branchLen, t):
    t.forward(branchLen)
    if branchLen > 5:
        t.right(20)
        fractalTree2(branchLen - 15, t)
        t.left(20)
        t.backward(branchLen)
    if branchLen > 5:
        t.left(20)
        fractalTree2(branchLen - 15, t)
        t.right(20)

def tree2(branchLen, t):
    t.forward(branchLen)
    if branchLen > 5:
        t.right(20)
        tree2(branchLen - 15, t)
        t.left(20)
        t.backward(branchLen)
    if branchLen > 5:
        t.left(20)
        tree2(branchLen - 15, t)
        t.right(20)

def fractalTree(branchLen, t):
    if branchLen > 0:
        t.forward(branchLen)
        t.right(20)
        fractalTree(branchLen - 15, t)
        t.left(40)
        fractalTree(branchLen - 15, t)
        t.right(20)
        t.backward(branchLen)

if __name__ == '__main__':
    t = Turtle()  # 创建画布实例
    t.screen.delay(0)  # 设置绘制显示延迟，以便观察过程
    
    # 初始化画笔
    t.pensize(2)  # 设置画笔粗细为 2 个像素
    t.color('green')  # 设置画笔颜色为 绿色
    t.left(90)  # 向左旋转 90 度，即让画笔朝上
    t.up()  # 抬起画笔，即在移动时不会绘制
    t.backward(300)  # 相对画笔朝向，向后退 300 个像素
    t.down()  # 落下画笔，准备绘制
    
    fractalTree2(130, t)  # 绘制分形树，根树干长度为 105 像素

    # 获取画布窗口，并设置关闭条件为点击窗口，以便在执行完成后保留绘图窗口
    t.getscreen().exitonclick()  


