#!/usr/bin/env python3
# -*- coding: utf-8 -*-

lis = []
for i in range(1, 10):
    lis.append(i*i)
print(lis)

lis = [x * x for x in range(1, 10)]
print(list)

list = [x * y for x in range(1, 10) for y in range(1, 10)]
print(lis)

lis = [i for i in range(1, 11) if i % 2 == 0]
print(lis) # [2, 4, 6, 8, 10]

dic = {x: x/2 for x in range(1,11) if x % 2 == 0}
print(dic)

dic = {'half': x/2 for x in range(1,11) if x % 2 == 0}
print(dic)

set1 = {x for x in range(10) if x % 2 == 0}
print(set1)

tup=(x for x in range(1,10))
print(tup)

tup=tuple(x for x in range(1,10))
print(tup) 




















