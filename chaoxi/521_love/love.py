import matplotlib.pyplot as plt
import seaborn
import numpy

# 定义方法
def draw_love():
 #拼凑字母
    l = numpy.arange(0, 4, 0.01)
    L = 1.0 / l
    theta = numpy.arange(-4, 4, 0.01)
    o = 3.0 * numpy.cos(theta)
    O = 3.0 * numpy.sin(theta)
    v = numpy.arange(-4, 4, 0.01)
    V = numpy.abs(-2.0 * v)
    e = numpy.arange(-3, 3, 0.01)
    E = -1.0 * numpy.abs(numpy.sin(e))
    y = numpy.arange(-10, 10, 0.01)
    Y = numpy.log2(numpy.abs(y))
    u = numpy.arange(-4, 4, 0.01)
    U = 2.0 * u ** 2
    points = []

    for heartY in numpy.linspace(-100, 100, 500):
        for heartX in numpy.linspace(-100, 100, 500):
            if ((heartX * 0.03) ** 2 + (heartY * 0.03) ** 2 - 1) ** 3 - (heartX * 0.03) ** 2 * (
                    heartY * 0.03) ** 3 <= 0:
                points.append({"x": heartX, "y": heartY})
# 设置直角坐标系
    heart_x = list(map(lambda point: point["x"], points))
    heart_y = list(map(lambda point: point["y"], points))

# 添加网格
    fig = plt.figure(figsize=(13, 7))
    ax_L = fig.add_subplot(2, 4, 1)
    ax_O = fig.add_subplot(2, 4, 2)
    ax_V = fig.add_subplot(2, 4, 3)
    ax_E = fig.add_subplot(2, 4, 4)
    ax_Y = fig.add_subplot(2, 4, 5)
    ax_O_2 = fig.add_subplot(2, 4, 6)
    ax_U = fig.add_subplot(2, 4, 7)
    ax_heart = fig.add_subplot(2, 4, 8)

    # 设置坐标
    ax_L.plot(l, L)
    ax_O.plot(o, O)
    ax_V.plot(v, V)
    ax_E.plot(E, e)
    ax_Y.plot(y, Y)
    ax_Y.axis([-10.0, 10.0, -10.0, 5.0])
    ax_O_2.plot(o, O)

    ax_U.plot(u, U)

    ax_heart.scatter(heart_x, heart_y, s=10, alpha=0.5)
 # 设置颜色
    plt.plot(color='red')
 # 展示结果
    plt.show()

# 主函数
if __name__ == '__main__':
    seaborn.set_style('dark')
    draw_love()