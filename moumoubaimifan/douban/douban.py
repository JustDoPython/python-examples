import json
import requests
import time
import random
import cpca
import jieba
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.charts import Geo
from pyecharts.globals import ChartType
from collections import Counter

addr_dic = {}
text_list = []

def main():
  url_basic = 'https://m.douban.com/rexxar/api/v2/gallery/topic/18306/items?from_web=1&sort=hot&start={}&count=20&status_full_text=1&guest_only=0&ck=GStY'
  headers = { 
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'bid=n7vzKfXLoUA; douban-fav-remind=1; ll="108296"; __utmc=30149280; __utmz=30149280.1624276858.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); ap_v=0,6.0; gr_user_id=ca8b9156-1926-4c82-9dda-27fc7f7ad51b; __utma=30149280.66080894.1623848440.1624276858.1624282580.3; __utmt=1; dbcl2="157316158:e4ojS8paSUc"; ck=GStY; push_doumail_num=0; __utmv=30149280.15731; frodotk="a187943e3a17e8bbe496bcbaae47ba31"; push_noty_num=0; __utmb=30149280.11.10.1624282580',
    'Host': 'm.douban.com',
    'Origin': 'https://www.douban.com',
    'Referer': 'https://www.douban.com/gallery/topic/18306/',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'
  }

  for i in range(1,35):
    
    res = requests.get(url=url_basic.format(i * 20), headers=headers)
    res_json = json.loads(res.text)
    print("这是第 {} 页".format(i * 20))
    index = 0
    for item in res_json.get('items'):
      target = item.get('target')
      status = target.get('status')
      print("这里是第 {} 个".format((i - 1) * 20 + index));
      index = index + 1
      with open('douban.txt', 'a+') as f:
        f.write(json.dumps(status) + '\n');

    sleeptime=random.randint(1, 10)
    time.sleep(sleeptime)


def readfile():
  file_object = open('douban.txt','r')
  try:
    for line in file_object:
      item = json.loads(line)
      if item == None:
        continue
      author = item['author']
      text = item['text']
      images = item['images']
      id = item['id']

      addr_transform = cpca.transform([text])
      addr = None

      if addr_transform['省'].str.split(' ')[0] != None:
        addr = addr_transform['省'].str.split(' ')[0][0].rstrip('省')
    
      if addr is None and author['loc'] is not None:
        cpca.transform([author['loc']['name']])
        if addr_transform['省'].str.split(' ')[0] != None:
            addr = addr_transform['省'].str.split(' ')[0][0].rstrip('省')
      
      if addr is not None:
        if addr == '广西壮族自治区':
          addr = '广西'
        if addr == '香港特别行政区':
          addr = '香港'
        if addr == '澳门特别行政区':
          addr = '澳门'
        addr_dic[addr] = addr_dic.get(addr, 0) + 1

        
      seg_list = jieba.cut(text, cut_all=False)
      text_list.extend(seg_list)

      index = 0
      for i in images:
        index = index + 1
        url = i.get('large').get('url')
        r = requests.get(url);
        with open('./image/{}-{}.jpg'.format(id, index), 'wb') as f:
          f.write(r.content)  

    
  finally:
    file_object.close()

  

  

def ciyun():
  # 词频统计,使用Count计数方法
  words_counter = Counter(text_list)
  # 将Counter类型转换为列表
  words = words_counter.most_common(500)

  (
    WordCloud()
    .add(series_name="", data_pair=words, word_size_range=[20, 66])
    .render("词云.html")
  )

def relitu():
  (
      Geo()
      .add_schema(maptype="china")
      .add(
          "",
          [list(z) for z in zip(list(addr_dic.keys()), list(addr_dic.values()))],
          type_=ChartType.HEATMAP,
      )
      .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
      .set_global_opts(
          visualmap_opts=opts.VisualMapOpts(),
      ).render("热力图.html")
  )

if __name__ == '__main__':
  main()
  readfile()
  relitu()
  ciyun()
