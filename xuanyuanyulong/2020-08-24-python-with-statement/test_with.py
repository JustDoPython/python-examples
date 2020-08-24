with open("test.txt", "r", encoding="utf-8") as f:
    s = f.readlines()


print(s)

# try:
#     f = open("test.txt", "a", encoding="utf-8")
#     s = f.readlines()
# except:
#     print("出现异常")
# finally:
#     f.close()