# get_heros.py
# 引入模块 
import requests 
import json 
import os
import time
 
st = time.time()    #程序开始时间
url = 'http://pvp.qq.com/web201605/js/herolist.json'
response=requests.get(url).content
 
# 提取Json信息
jsonData=json.loads(response) 
print(jsonData)

# 初始化下载数量 
x = 0 
 
#目录不存在则创建 
hero_dir='/Users/mm/python/python-examples/heros/imgs/' 
if not os.path.exists(hero_dir):
     os.mkdir(hero_dir)
 
for m in range(len(jsonData)):
    # 英雄编号 
    ename = jsonData[m]['ename'] 
    # 英雄名称 
    cname = jsonData[m]['cname']  
    # 皮肤名称，一般英雄会有多个皮肤 
    skinName = jsonData[m]['skin_name'].split('|') 
    # 皮肤数量 
    skinNumber = len(skinName)
 
    # 循环遍历处理
    for bigskin in range(1,skinNumber+1):
        # 拼接下载图片url
        picUrl = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'+str(ename)+'/'+str(ename)+'-bigskin-'+str(bigskin)+'.jpg'
        #获取图片内容 
        picture = requests.get(picUrl).content 
        # 保存图片 
        with open( hero_dir + cname + "-" + skinName[bigskin-1]+'.jpg','wb') as f:
            f.write(picture)
            x=x+1
            print("当前下载第"+str(x)+"张皮肤")   
# 获取结束时间 
end = time.time()
# 计算执行时间
exec_time = end-st 
print("找到并下载"+str(x)+"张图片,总共用时"+str(exec_time)+"秒。")
