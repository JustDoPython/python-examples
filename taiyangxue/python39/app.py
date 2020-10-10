## 字典合并
d1 = {'a': 'A', 'b': 'B', 'c': 'C'}
d2 = {'d': 'D', 'e': 'E'}

# 旧版
d3 = {**d1, **d2}  # 使用展开操作符，将合并结果存入 d3
print(d3)  # {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E'}

d1.update(d2)  # update 方法，将 d1 d2 合并，且更新 d1
print(d1)  # {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E'}

# 新版
d3 = d1 | d2  # 效果等同于展开操作符
print(d3)  # {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E'}

d1 |= d2  # 等同于 update
print(d1)  # {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E'}


## 拓扑排序
from graphlib import TopologicalSorter

tg = {5: {3, 4}, 4: {2, 3}, 3: {2, 1}, 2: {1}}
ts = TopologicalSorter(tg)

print(list(ts.static_order())) # [1, 2, 3, 4, 5]

ts = TopologicalSorter()
ts.add(5, 3, 4)
ts.add(4, 2, 3)
ts.add(3, 2, 1)
ts.add(2, 1)

print(list(ts.static_order())) # [1, 2, 3, 4, 5]


## 随机字节码
import random
print(random.randbytes(10))  # b'\x0fzf\x17K\x00\xfb\x11LF'  随机的，每次结果可能不同


## 最小公倍数
import math
math.lcm(49, 14)  # 98

def lcm(num1, num2):
  if num1 == num2 == 0:
    return 0
  return num1 * num2 // math.gcd(num1, num2)

lcm(49, 14)  # 98


## 字符串去前后缀
"three cool features in Python".removesuffix(" Python")
# three cool features in

"three cool features in Python".removeprefix("three ")
# cool features in Python

"three cool features in Python".removeprefix("Something else")
# three cool features in Python


## 时区
from zoneinfo import ZoneInfo
from datetime import datetime

dt = datetime(2020, 10, 1, 1, tzinfo= ZoneInfo("America/Los_Angeles"))