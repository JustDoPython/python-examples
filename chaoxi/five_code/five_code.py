# 5 行代码写服务器
from http import server
from http.server import SimpleHTTPRequestHandler
server_address = ('127.0.0.1', 8080)
httpd = server.HTTPServer(server_address, SimpleHTTPRequestHandler)
httpd.serve_forever()


# 加法计算器
num1 = input("第一个数：")
num2 = input("第二个数：")
new_num1 = int(num1)
new_num2 = int(num2)
print(new_num1 + new_num2)

# 兔子问题
# #古典问题：有一对兔子，从出生后第3个月起每个月都生一对兔子，小兔子长到第三个月后每个月又生一对兔子，假如兔子都不死，问每个月的兔子总数为多少？
def count(n):
    if (1 == n or 2 == n):
        return 1
    elif (n >= 2):
        return count(n - 2) + count(n - 1)
print(count(36) * 2)


# 吗呢问答
while(True):
    question = input()
    answer = question.replace('吗', '呢')
    answer = answer.replace('？', '！')
    print(answer)


#  九九乘法表1
for i in range(1, 10):
    for j in range(1, i+1):
        print('{}x{}={}\t'.format(j, i, i*j), end='')
    print()

# 九九乘法表 2
for i in range(1, 10):
    for j in range(i, 10):
        print(f'{i}x{j}={i*j}',end='\t')
    print(" ")
print("\n")

# 逆序打印数字
def nixu(n):
    l = str(n)
    l_str = l[::-1]
    print("逆序:%s" % ( l_str))
nixu(2020)


from wordcloud import WordCloud
import PIL.Image as image

with open('wordcloud.txt') as fp:
    text = fp.read()
    wordcloud = WordCloud().generate(text)
    img = wordcloud.to_image()
    img.show()

# 快捷二维码生成
from MyQR import myqr
myqr.run(
    words='https://www.baidu.com/',
    colorized=True,
    save_name='baidu_code.png')


