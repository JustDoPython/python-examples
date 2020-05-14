# 心形字符
print('\n'.join([''.join([('Python技术'[(x-y)%len('Python技术')] if((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3<=0 else' ')for x in range(-30,30)])for y in range(15,-15,-1)]))

# 9*9乘法口诀表
print('\n'.join([' '.join(['%s*%s=%-2s' % (y, x, x*y) for y in range(1, x+1)]) for x in range(1, 10)]))

print('\n')

# 斐波拉契数列
print([x[0] for x in [(a[i][0], a.append([a[i][1],a[i][0]+a[i][1]])) for a in ([[1,1]], ) for i in range(30)]])

print('\n')

# 解决FizzBuzz问题
for x in range(1,101): print("fizz"[x%3*4:]+"buzz"[x%5*4:] or x)

print('\n')

# Mandelbrot图像
print('\n'.join([''.join(['*'if abs((lambda a: lambda z,c,n:a(a,z,c,n))(lambda s,z,c,n:z if n==0 else s(s,z*z+c,c,n-1))(0,0.02*x+0.05j*y,40))<2 else ' ' for x in range(-80,20)]) for y in range(-20,20)]))

print('\n')

# 计算出1-1000之间的素数
print(' '.join([str(item) for item in filter(lambda x: not [x%i for i in range(2,x) if x%i==0],range(2,1001))]))

print('\n')

# 解决八皇后问题
[__import__('sys').stdout.write('\n'.join('.'*i+'Q'+'.'*(8-i-1) for i in vec)+"\n========\n") for vec in __import__('itertools').permutations(range(8)) if 8==len(set(vec[i]+i for i in range(8)))==len(set(vec[i]-i for i in range(8)))]

print('\n')

# 生成迷宫
print(''.join(__import__('random').choice('\u2571\u2572') for i in range(50*24)))

