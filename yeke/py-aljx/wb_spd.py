import re
import time
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 爬取一页评论内容
def get_one_page(url):
    headers = {
        'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3880.4 Safari/537.36',
        'Host' : 'weibo.cn',
        'Accept' : 'application/json, text/plain, */*',
        'Accept-Language' : 'zh-CN,zh;q=0.9',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Cookie' : '自己的Cookie',
        'DNT' : '1',
        'Connection' : 'keep-alive'
    }
    # 获取网页 html
    response = requests.get(url, headers = headers, verify=False)
    # 爬取成功
    if response.status_code == 200:
        # 返回值为 html 文档，传入到解析函数当中
        return response.text
    return None

# 解析保存评论信息
def save_one_page(html):
    comments = re.findall('<span class="ctt">(.*?)</span>', html)
    for comment in comments[1:]:
        result = re.sub('<.*?>', '', comment)
        if '回复@' not in result:
            with open('aljx.txt', 'a+', encoding='utf-8') as fp:
                fp.write(result)

for i in range(100):
    url = 'https://weibo.cn/comment/JfHax8BpP?uid=2357213493&rl=0&page='+str(i)
    html = get_one_page(url)
    print('正在爬取第 %d 页评论' % (i+1))
    save_one_page(html)
    time.sleep(3)