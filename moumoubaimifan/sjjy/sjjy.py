# coding:utf-8
import csv
import json

import requests
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
import re

line_index = 0

def fetchURL(url):
   
    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'Cookie': 'guider_quick_search=on; accessID=20201021004216238222; PHPSESSID=11117cc60f4dcafd131b69d542987a46; is_searchv2=1; SESSION_HASH=8f93eeb87a87af01198f418aa59bccad9dbe5c13; user_access=1; Qs_lvt_336351=1603457224; Qs_pv_336351=4391272815204901400%2C3043552944961503700'
    }

    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.text.encode("gbk", 'ignore').decode("gbk", "ignore")


def parseHtml(html):

    html = html.replace('\\', '')
    html = ILLEGAL_CHARACTERS_RE.sub(r'', html)
    s = json.loads(html,strict=False)
    global line_index

    userInfo = []
    for key in s['userInfo']:
        line_index = line_index + 1
        a = (key['uid'],key['nickname'],key['age'],key['work_location'],key['height'],key['education'],key['matchCondition'],key['marriage'],key['shortnote'].replace('\n',' '))
        userInfo.append(a)

    with open('sjjy.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(userInfo)

def filterData():
    filter = []
    csv_reader = csv.reader(open("sjjy.csv", encoding='gbk'))
    i = 0
    for row in csv_reader:
        i = i + 1
        print('正在处理：' + str(i) + '行')
        if row[0] not in filter:
            filter.append(row[0])
    print(len(filter))

if __name__ == '__main__':
    
    # for i in range(1, 10000):
    #     url = 'http://search.jiayuan.com/v2/search_v2.php?key=&sex=f&stc=23:1,2:20.30&sn=default&sv=1&p=' + str(i) + '&f=select&listStyle=bigPhoto'
    #     html = fetchURL(url)
    #     print(str(i) + '页' + str(len(html)) + '*********' * 20)
    #     parseHtml(html)
    filterData()
