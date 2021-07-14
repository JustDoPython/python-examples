import random

anger_face = ["ಠ_ಠ","ノಠ_ಠノ","(¬_¬)", "(┳◇┳)","(◔ д◔)","(ʘдʘ╬)","(눈_눈)","-`д´-"]

num = random.randint(0,10)
while(True):
  n = input("请输入：")
  if not n.isdecimal():
      print(random.choice(anger_face))
      continue

  n = int(n)
  if num == n:
      print("你赢啦！！！\n\n")
      break
  elif num < n:
      print("大")
  else:
      print("小")