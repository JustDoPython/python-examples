import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
# 指定图形类型为 3d 类型
ax = fig.add_subplot(111, projection='3d')
# X, Y value
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)

# 设置 x-y 平面的网格
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X ** 2 + Y ** 2)
# height value
Z = np.sin(R)

# rstride:行之间的跨度  cstride:列之间的跨度
# rcount:设置间隔个数，默认50个，ccount:列的间隔个数  不能与上面两个参数同时出现
#vmax和vmin  颜色的最大值和最小值
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('rainbow'))

# zdir : 'z' | 'x' | 'y' 表示把等高线图投射到哪个面
# offset : 表示等高线图投射到指定页面的某个刻度
ax.contourf(X,Y,Z,zdir='z',offset=-2)

# 设置图像z轴的显示范围，x、y轴设置方式相同
ax.set_zlim(-2,2)

plt.show()