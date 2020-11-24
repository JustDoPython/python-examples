import csv
import re
from functools import reduce

import requests
import json
import time
from pathlib import Path

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
import jieba
import wordcloud

import ssl
ssl._create_default_https_context=ssl._create_unverified_context

# csv保存函数
def csv_write(tablelist):
    tableheader = ['弹幕内容', '情感']
    csv_file = Path('danmu.csv')
    not_file = not csv_file.is_file()
    with open('danmu.csv', 'a', newline='', errors='ignore') as f:
        writer = csv.writer(f)
        if not_file:
            writer.writerow(tableheader)
        for row in tablelist:
            writer.writerow(row)

def nlp(text):
    try:
        cred = credential.Credential("xxx", "xxx")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "nlp.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)

        req = models.SentimentAnalysisRequest()
        params = {
            "Text": text,
            "Mode": "3class"
        }
        req.from_json_string(json.dumps(params))

        resp = client.SentimentAnalysis(req)
        sentiment = {'positive': '正面', 'negative': '负面', 'neutral': '中性'}
        return sentiment[resp.Sentiment]
    except TencentCloudSDKException as err:
        print(err)

# df = pd.DataFrame()
def danmu():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36'
    }
    urls = [['https://mfm.video.qq.com/danmu?otype=json&callback=&target_id=6208914107%26vid%3Do0035t7199o&session_key=63761%2C673%2C1606144955&timestamp={}&_=1606144949402', 7478],
            ['https://mfm.video.qq.com/danmu?otype=json&callback=&target_id=6208234802%26vid%3Da00352eyo25&session_key=111028%2C1191%2C1606200649&timestamp={}&_=1606200643186', 8610]]

    for url in urls:
        for page in range(15, url[1], 30):
            u = url[0].format(page)
            html = requests.get(u, headers=headers)
            result = json.loads(html.text, strict=False)
            time.sleep(1)
            danmu_list = []
            # 遍历获取目标字段
            for i in result['comments']:
                content = i['content']  # 弹幕内容
                n = nlp(content)
                danmu_list.append([content, n])
                print(content)
            csv_write(danmu_list)

def analysis():
    guest = {'陈凯歌,陈导,凯歌':{'正面':0,'负面':0,'中性':0},
             '尔冬升,尔导':{'正面':0,'负面':0,'中性':0},
             '赵薇,薇导':{'正面':0,'负面':0,'中性':0},
             '郭敬明,郭导,小四':{'正面':0,'负面':0,'中性':0},
             '大鹏':{'正面':0,'负面':0,'中性':0}}

    with open('danmu.csv') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            for g in guest.keys():
                for i in g.split(','):
                    a = [m.start() for m in re.finditer(i, row[0])]
                    if len(a) != 0:
                        guest[g][row[1]] = guest.get(g).get(row[1]) + 1
    return guest

def draw(guest = {}):

    list1 = [
        {"value": guest.get('陈凯歌,陈导,凯歌').get('正面'), "percent": guest.get('陈凯歌,陈导,凯歌').get('正面') / reduce(lambda x,y:x+y,guest.get('陈凯歌,陈导,凯歌').values())},
        {"value": guest.get('尔冬升,尔导').get('正面'), "percent": guest.get('尔冬升,尔导').get('正面') / reduce(lambda x,y:x+y,guest.get('尔冬升,尔导').values())},
        {"value": guest.get('赵薇,薇导').get('正面'), "percent": guest.get('赵薇,薇导').get('正面') / reduce(lambda x,y:x+y,guest.get('赵薇,薇导').values())},
        {"value": guest.get('郭敬明,郭导,小四').get('正面'), "percent": guest.get('郭敬明,郭导,小四').get('正面') / reduce(lambda x,y:x+y,guest.get('郭敬明,郭导,小四').values())},
        {"value": guest.get('大鹏').get('正面'), "percent": guest.get('大鹏').get('正面') / reduce(lambda x,y:x+y,guest.get('大鹏').values())},
    ]
    list2 = [
        {"value": guest.get('陈凯歌,陈导,凯歌').get('负面'),
         "percent": guest.get('陈凯歌,陈导,凯歌').get('负面') / reduce(lambda x, y: x + y, guest.get('陈凯歌,陈导,凯歌').values())},
        {"value": guest.get('尔冬升,尔导').get('负面'),
         "percent": guest.get('尔冬升,尔导').get('负面') / reduce(lambda x, y: x + y, guest.get('尔冬升,尔导').values())},
        {"value": guest.get('赵薇,薇导').get('负面'),
         "percent": guest.get('赵薇,薇导').get('负面') / reduce(lambda x, y: x + y, guest.get('赵薇,薇导').values())},
        {"value": guest.get('郭敬明,郭导,小四').get('负面'),
         "percent": guest.get('郭敬明,郭导,小四').get('负面') / reduce(lambda x, y: x + y, guest.get('郭敬明,郭导,小四').values())},
        {"value": guest.get('大鹏').get('负面'),
         "percent": guest.get('大鹏').get('负面') / reduce(lambda x, y: x + y, guest.get('大鹏').values())},
    ]

    list3 = [
        {"value": guest.get('陈凯歌,陈导,凯歌').get('中性'),
         "percent": guest.get('陈凯歌,陈导,凯歌').get('中性') / reduce(lambda x, y: x + y, guest.get('陈凯歌,陈导,凯歌').values())},
        {"value": guest.get('尔冬升,尔导').get('中性'),
         "percent": guest.get('尔冬升,尔导').get('中性') / reduce(lambda x, y: x + y, guest.get('尔冬升,尔导').values())},
        {"value": guest.get('赵薇,薇导').get('中性'),
         "percent": guest.get('赵薇,薇导').get('中性') / reduce(lambda x, y: x + y, guest.get('赵薇,薇导').values())},
        {"value": guest.get('郭敬明,郭导,小四').get('中性'),
         "percent": guest.get('郭敬明,郭导,小四').get('中性') / reduce(lambda x, y: x + y, guest.get('郭敬明,郭导,小四').values())},
        {"value": guest.get('大鹏').get('中性'),
         "percent": guest.get('大鹏').get('中性') / reduce(lambda x, y: x + y, guest.get('大鹏').values())},
    ]

    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(['陈凯歌', '尔冬升', '赵薇', '郭敬明', '大鹏'])
            .add_yaxis("正面", list1, stack="stack1", category_gap="50%")
            .add_yaxis("负面", list2, stack="stack1", category_gap="50%")
            .add_yaxis("中性", list3, stack="stack1", category_gap="50%")
            .set_series_opts(
            label_opts=opts.LabelOpts(
                position="right",
                formatter=JsCode(
                    "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"
                ),
            )
        )
            .render("导演.html")
    )


def ciyun():
    with open('danmu.csv') as f:
        with open('ciyun.txt', 'a') as ciyun_file:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                ciyun_file.write(row[0])

    # 构建并配置词云对象w
    w = wordcloud.WordCloud(width=1000,
                            height=700,
                            background_color='white',
                            font_path="/System/Library/fonts/PingFang.ttc",
                            collocations=False,
                            stopwords={'的', '了','啊','我','很','是','好','这','都','不'})


    f = open('ciyun.txt', encoding='utf-8')
    txt = f.read()
    txtlist = jieba.lcut(txt)
    result = " ".join(txtlist)

    w.generate(result)

    w.to_file('演员请就位2.png')


if __name__ == "__main__":
    ciyun()