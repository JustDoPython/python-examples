import random
import requests
from bs4 import BeautifulSoup
import re
import math

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

def create_headers():
    headers = dict()
    headers["User-Agent"] = random.choice(USER_AGENTS)
    headers["Referer"] = "http://www.ke.com"
    return headers

class NewHouse(object):
    def __init__(self, xiaoqu, price, total):
        self.xiaoqu = xiaoqu
        self.price = price
        self.total = total

    def text(self):
        return self.xiaoqu + "," + \
                self.price + "," + \
                self.total

with open("newhouse.txt", "w", encoding='utf-8') as f:
    # 开始获得需要的板块数据
    total_page = 1
    loupan_list = list()
    page = 'http://bj.fang.ke.com/loupan/'
    print(page)
    headers = create_headers()
    response = requests.get(page, timeout=10, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, "lxml")

    # 获得总的页数
    try:
        page_box = soup.find_all('div', class_='page-box')[0]
        matches = re.search('.*data-total-count="(\d+)".*', str(page_box))
        total_page = int(math.ceil(int(matches.group(1)) / 10))
    except Exception as e:
        print(e)

    print(total_page)
    # 从第一页开始,一直遍历到最后一页
    headers = create_headers()
    for i in range(1, total_page + 1):
        page = 'http://bj.fang.ke.com/loupan/pg{0}'.format(i)
        print(page)
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得有小区信息的panel
        house_elements = soup.find_all('li', class_="resblock-list")
        for house_elem in house_elements:
            price = house_elem.find('span', class_="number")
            desc = house_elem.find('span', class_="desc")
            total = house_elem.find('div', class_="second")
            loupan = house_elem.find('a', class_='name')

            # 继续清理数据
            try:
                price = price.text.strip() + desc.text.strip()
            except Exception as e:
                price = '0'

            loupan = loupan.text.replace("\n", "")

            try:
                total = total.text.strip().replace(u'总价', '')
                total = total.replace(u'/套起', '')
            except Exception as e:
                total = '0'

            # 作为对象保存
            loupan = NewHouse(loupan, price, total)
            print(loupan.text())
            loupan_list.append(loupan)

    for loupan in loupan_list:
        f.write(loupan.text() + "\n")

