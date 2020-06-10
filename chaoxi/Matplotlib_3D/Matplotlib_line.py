import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 依次获取画布和绘图区并创建 Axes3D 对象
fig = plt.figure()
ax = fig.gca(projection='3d')

# 第一条3D线性图数据
theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z1 = np.linspace(-2, 2, 100)
r = z1**2 + 1
x1 = r * np.sin(theta)
y1 = r * np.cos(theta)

# 第二条3D线性图数据
z2 = np.linspace(-3, 3, 100)
x2 = np.sin(z2)
y2 = np.cos(z2)

# 绘制3D线性图
ax.plot(x1, y1, z1, color='b', label='3D Line1')
ax.plot(x2, y2, z2, color='r', label='3D Line2')

# 设置标题、轴标签、图例，也可以直接使用 plt.title、plt.xlabel、plt.legend...
ax.set_title('3D Line View', pad=15, fontsize='10')
ax.set_xlabel('x ', color='r', fontsize='14')
ax.set_ylabel('y ', color='g', fontsize='14')
ax.set_zlabel('z ', color='b', fontsize='14')
ax.legend()
plt.show()
