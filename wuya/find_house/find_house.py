import pandas as pd
import requests
import json
import csv
import codecs

# 创建导出文件
with open(r'..\document\village.csv', 'wb+')as fp:
    fp.write(codecs.BOM_UTF8)
f = open(r'..\document\village.csv','w+',newline='', encoding='utf-8')
writer = csv.writer(f)
writer.writerow(("小区名", "坐标", "步行距离-地点1","通勤时间-地点1", "步行距离-地点2","通勤时间-地点2"))

geourl = 'https://restapi.amap.com/v3/geocode/geo'  
puburl = 'https://restapi.amap.com/v3/direction/transit/integrated?origin={}&destination={}&key={}&time=9:00&city=上海'  

# 读取文件
csv_read=pd.read_csv('../document/sh.csv',header=None)
village_set = set(csv_read[2])
village_list = list(village_set)

# 获取第一个坐标
geourl = 'https://restapi.amap.com/v3/geocode/geo'  
# 地址前要加地区名，否则可能定位到其他城市
params = {'key':'在这里填入个人的Key值',
        'address': '上海市国金中心'}
# 发送请求                
res = requests.get(geourl, params)
jd = json.loads(res.text)
# 返回值的具体格式可以在API文档中查看
geopoint_1 = jd['geocodes'][0]['location']

# 获取第二个坐标
params = {'key':'在这里填入个人的Key值',
        'address': '上海市国正中心'}               
res = requests.get(geourl, params)
jd = json.loads(res.text)
geopoint_2 = jd['geocodes'][0]['location']

for adr in village_list:
    # 获取小区坐标
    params = {'key':'在这里填入个人的Key值',
        'address': '上海市'+adr}                
    res = requests.get(geourl, params)
    jd = json.loads(res.text)
    geopoint = jd['geocodes'][0]['location']

    # 获取第一个位置的信息
    r=requests.get(puburl.format(geopoint_1, geopoint, '在这里填入个人的Key值'))  
    r=r.text  
    jsonData=json.loads(r)
    publength_1 = round(int(jsonData['route']['transits'][0]['walking_distance'])/1000, 2)
    pubtime_1 = round(int(jsonData['route']['transits'][0]['duration'])/60)  

    # 获取第二个位置的信息
    r=requests.get(puburl.format(geopoint_2, geopoint, '在这里填入个人的Key值'))  
    r=r.text  
    jsonData=json.loads(r)
    publength_2 = round(int(jsonData['route']['transits'][0]['walking_distance'])/1000, 2)
    pubtime_2 = round(int(jsonData['route']['transits'][0]['duration'])/60)  

    writer.writerow((adr, geopoint, publength_1, pubtime_1, publength_2, pubtime_2))

f.close()