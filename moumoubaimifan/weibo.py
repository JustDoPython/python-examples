# 爬虫命令
# python3 -m weibo_spider

from aip import AipNlp
import csv
import time
import re

APP_ID = 'APP_ID'
API_KEY = 'API_KEY'
SECRET_KEY = 'SECRET_KEY'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


file = open("D:\\weibo\\weibo\\宫崎骏漫画全集\\3733371872.csv", "r", encoding="utf-8", errors='ignore')
reader = csv.reader(file)
result = {'good':0,'bed':-1}
hanzi = re.compile('[\u4e00-\u9fa5 0-9?？。.,，]')
for item in reader:
    time.sleep(1)
    a = "".join(hanzi.findall(item[1]))
    if len(a.encode()) > 1024:
        continue
  
    sent = client.sentimentClassify(a)

    items = sent['items'][0]
    if items["positive_prob"] > items["negative_prob"]:
        result['good'] = result['good'] + 1
    else:
        result['bed'] = result['bed'] + 1
    
print('微博内容总共：{} 条，好心情：{}，差心情：{}'.format(result['good'] + result['bed'], result['good'], result['bed']))
if(result['good'] > result['bed']):
    print('最近女神心情好，建议发出约会要求')
else:
    print('最近女神心情非常差，建议吃大餐')
