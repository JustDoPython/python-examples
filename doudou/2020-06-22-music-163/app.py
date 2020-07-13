import requests
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# 模拟浏览器请求
headers = {
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    'Accept': '*/*',
}

# 构建 URL 以及 POSt 参数
url = 'https://music.163.com/weapi/v1/play/record?csrf_token='
data = {
    'params': 'xrJhjXYUqEWa98DVbFtw6yTygOTCOvSAypxfWNr5kpw/MEvXsRk+Av+DNF7zY9a1oA95FsmDtE3VpM422dZR6WJGDxS3/se00qFFHx6wumfLzc9mgnfB5hGkrBwF9+P/7zamjfWSOUfvvUuWhM2Gd7z2pA11lMB',
    'encSecKey': '2371bb4de91d5de7110722d3491c7cf6d3f6f5cdcbc16a5e9c7456e4b9075c1965bbd2bf4fbf02023cf63391f74b6956339cb72fa32a4413de347ffb536299f5711fe02fe60f66b77ac96a16a6bcb5ba14cf9b1609ddf8e8180d683bba5801acf'
}

# 发送请求
req = requests.post(url, data)  # 发送 post 请求，第一个参数是 URL，第二个参数是参数

print(json.loads(req.text))

# 输出结果
# {"allData":[{"playCount":0,"score":100,"song":{"name":"盛夏光年 (2013版)","id":28181110,"pst":0,"t":0,"ar":[{"id":13193,"name":"五月天","tns":...

result = json.loads(req.text)
names = []
for i in range(100):
    names.append(result['allData'][i]['song']['ar'][0]['name'])

text = ",".join(names)


def show_word_cloud(text):
    wc = WordCloud(font_path='/System/Library/Fonts/PingFang.ttc', background_color="white", scale=2.5,
                   contour_color="lightblue", ).generate(text)

    # 读入背景图片
    w = WordCloud(background_color='white', scale=1.5).generate(text)
    w.to_file("names.png")
    plt.figure(figsize=(16, 9))
    plt.imshow(wc)
    plt.axis('off')
    plt.show()


show_word_cloud(text)