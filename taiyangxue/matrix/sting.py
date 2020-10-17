# 命令行下执行

a = "some_string"
id(a)
id("some" + "_" + "string") # 不同方式创建的字符串实质是一样的.

a = "wtf"
b = "wtf"
a is b  # 想想结果是什么

a = "wtf!"
b = "wtf!"
a is b  # 结果又会是什么