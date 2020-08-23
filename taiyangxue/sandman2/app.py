
"""
创建mysql 数据库，将 sandman2_test_data.sql 导入

启动 sandman 服务器

sandman2ctl 'mysql+pymysql://bob:bobpasswd@localhost:3306/sandman2_test_data'
"""

import requests as rq
import json

## 返回 学生表 student 的所有记录
# curl http://localhost:5000/student/

data = rq.get("http://localhost:5000/student/").content
data = json.loads(data)
print("student 的所有记录")
print(data)

## 返回 学生表 student 的第一页数据
# curl http://localhost:5000/student/?page=1
data = rq.get("http://localhost:5000/student/?page=1").content
data = json.loads(data)
print("student 的第一页数据")
print(data)

## 获取 id 为 1 的学生记录
# curl http://localhost:5000/student/1
data = rq.get("http://localhost:5000/student/1").content
data = json.loads(data)
print("id 为 1 的学生记录")
print(data)

## 查询 `name` 为 Tom 的学生记录
# curl http://localhost:5000/student/?name=Tom
data = rq.get("http://localhost:5000/student/?name=Tom").content
data = json.loads(data)
print("查询 `name` 为 Tom 的学生记录")
print(data)

## 查询班级为 1 年龄为 18 的学生:
# curl http://localhost:5000/student/?class=1&age=19
data = rq.get("http://localhost:5000/student/?class=1&age=19").content
data = json.loads(data)
print("查询班级为 1 年龄为 18 的学生")
print(data)

## 增加一个学生信息
# curl -X POST -d '{"name": "Lily", "age": 17, "class":1, "profile":"Likely"}' -H "Content-Type: application/json" http://127.0.0.1:5000/student/
data = rq.post("http://127.0.0.1:5000/student/", headers={"Content-Type": "application/json"}, data='{"name": "Tiger", "age": 17, "class":2, "profile":"Handsame"}').content
data = json.loads(data)
print("增加一个学生信息")
print(data)

## id 为 1 的学生班级更改为 3
# curl -X PATCH -d '{"class":3}' -H "Content-Type: application/json" http://127.0.0.1:5000/student/1
data = rq.patch("http://127.0.0.1:5000/student/1", headers={"Content-Type": "application/json"}, data='{"class": 3}').content
data = json.loads(data)
print("id 为 1 的学生班级更改为 3")
print(data)

## 删除 id 为 11 的学生记录
# curl -X DELETE -H "Content-Type: application/json" http://127.0.0.1:5000/student/11
data = rq.delete("http://127.0.0.1:5000/student/11").content
print("删除 id 为 11 的学生记录")
print(data)

## 获取 学生表 student 的字段定义
# curl http://127.0.0.1:5000/student/meta
data = rq.get("http://localhost:5000/student/meta").content
data = json.loads(data)
print("获取 学生表 student 的字段定义")
print(data)

## 导出学生数据，存放到 student.csv 文件中
# curl -o student.csv http://127.0.0.1:5000/student/?export
r = rq.get("http://127.0.0.1:5000/student/?export") 
with open("student.csv",'wb') as f:
    f.write(r.content)
print("数据导出完毕")
