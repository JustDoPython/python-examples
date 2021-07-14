import random

num = random.randint(0,10)

while(True):
  n = input("请输入：")
  n = int(n)
  if num == n:
      print("你赢啦！！！\n\n")
      break
  elif num < n:
      print("大")
  else:
      print("小")