def outer(x):
    def inner(y):
        # 在内函数中 用到了外函数的变量
        nonlocal x
        x += y
        return x + y

    # 外函数的返回值是内函数的引用
    return inner

fun = outer(10)

print(fun(10)) # 30
print(fun(10)) # 40
print(fun(10)) # 50