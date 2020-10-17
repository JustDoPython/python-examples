# 命令行下执行
# 思考下下面表达式的值

(False == False) in [False] # 合乎常理
False == (False in [False]) # 也没问题
False == False in [False] # 现在感觉如何?
True is False == False
False is False is False
1 > 0 < 1
(1 > 0) < 1
1 > (0 < 1)