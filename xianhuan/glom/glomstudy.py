#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from glom import glom, Coalesce

d = {"a": {"b": {"c": 1}}}
print(glom(d, "a.b.c"))

d = {"a": {"b": None}}
# print(d["a"]["b"]["c"])
# print(glom(d, "a.b.c"))

data = {"student": {"info": [{"name": "张三"}, {"name": "李四"}]}}
info = glom(data, ("student.info", ["name"]))
print(info)

info = glom(data, {"info": ("student.info", ["name"])})
print(info) 


data_1 = {"school": {"student": [{"name": "张三"}, {"name": "李四"}]}}
data_2 = {"school": {"teacher": [{"name": "王老师"}, {"name": "赵老师"}]}}

spec_1 = {"name": ("school.student", ["name"])}
spec_2 = {"name": ("school.teacher", ["name"])}
print(glom(data_1, spec_1))
print(glom(data_2, spec_2))


spec = {"name": (Coalesce("school.student", "school.teacher"), ["name"])}
 
print(glom(data_1, spec))
print(glom(data_2, spec))       

data = {"school": {"student": [{"name": "张三", "age": 18}, {"name": "李四", "age": 20}]}}
spec = {"sum_age": ("school.student", ["age"], sum)}
print(glom(data, spec))
