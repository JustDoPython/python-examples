from bs4 import BeautifulSoup


# 文件 test.html 需由读者自行创建
with open("test.html", "r", encoding="utf-8") as f:
    content = f.read()

response = BeautifulSoup(content,'lxml')

results = response.find_all("b")

with open("SongList.txt", "w+", encoding="utf-8") as f:
    f.writelines([result["title"] + "\n" for result in results])