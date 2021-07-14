import random

anger_face = ["ಠ_ಠ","ノಠ_ಠノ","(¬_¬)", "(┳◇┳)","(◔ д◔)","(ʘдʘ╬)","(눈_눈)","-`д´-","😲","😱","😧"]

def game():
    print("( ＾∀＾）／欢迎＼( ＾∀＾）")
    num = random.randint(0,10)

    while(True):
        n = input(">>>>：")
        if not n.isdecimal():
            print(random.choice(anger_face))
            continue

        n = int(n)
        if num == n:
            print("✌ ('ω')")
            break
        elif num < n:
            print("大")
        else:
            print("小")

while(True):
    game()
    c = input("再来一把 (y)/n?")
    if c == "n":
        print("(ToT)/~~~")
        break