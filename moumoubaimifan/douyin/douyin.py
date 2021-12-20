import requests
import json
import os
import time
import re

headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Mobile Safari/537.36"
}

share = input('分享的链接：')

url = re.findall('(https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]+)', share)[0]


resp = requests.get(url=url, headers=headers, allow_redirects=False)

location = resp.headers['location']

temp = location.split('&')

sec_uid = temp[4].split('=')[1]

url = "https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid={}".format(sec_uid)
resp = requests.get(url, headers=headers)
userinfo = json.loads(resp.text)

name = userinfo['user_info']['nickname']

if os.path.exists(name) == False:
    os.mkdir(name)
os.chdir(name)


year = [2020,2021,2022]
cursor = []
for y in year:
    for i in range(1,13):
        calc = str(y) + '-'+ str(i) + '-' + '01 00:00:00'
        timeArray = time.strptime(calc, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray)) * 1000
        cursor.append(timeStamp)

for i in range(len(cursor) - 1):
    params = {
        "sec_uid": sec_uid,
        "count": 200,
        "min_cursor": cursor[i],
        "max_cursor": cursor[i+1],
        "_signature": "Sq1xlgAAK2.rxFYl7oQq7EqtcY"
    }

    url = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?'

    resp = requests.get(url=url, params=params, headers=headers)
    data = json.loads(resp.text)
    awemenum = data['aweme_list']
    for item in awemenum:
        title = re.sub('[\/:*?"<>|]','-',item['desc'])
        url = item['video']['play_addr']['url_list'][0]

        with open(title + ".mp4", 'wb') as f:
            f.write(requests.get(url, headers=headers).content)
            print(title + "------------------下载完成")
