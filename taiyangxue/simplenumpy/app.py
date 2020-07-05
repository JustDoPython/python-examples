import numpy as np

m = np.array([(1,2,3),(2,3,4),(3,4,5)])

print(m**2)

n = np.array([(1,2),(2,3),(3,4)])

print(m.dot(n))


# 求和
print(m.sum())
# 连乘
print(m.prod())

# 均值

x = np.array([1,2,3,4,5,6,7,8])

print((1/x.size)*x.sum())
print(x.sum()/x.size)

# 实现 Frobenius 范数
print(np.sqrt((m**2).sum()))

# 样本方差
print(np.sqrt(((x-(x.sum()/x.size))**2).sum()/(x.size-1)))
print(np.sqrt(((x-np.mean(x))**2).sum()/(x.size-1)))
# 标准差
print(np.sqrt(((x-np.mean(x))**2).sum()/x.size))
print(np.std(x))

# 欧拉距离
a = np.array([1,2,3,4,5,6])
b = np.array([2,3,4,5,6,7])
print(np.sqrt(((a-b)**2).sum()))
print(np.linalg.norm(a-b))