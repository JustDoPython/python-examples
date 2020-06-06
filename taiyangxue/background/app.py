
import base64
from bs4 import BeautifulSoup as BS
import baiduapi as bd
import httpx
from PIL import Image
import io
import difflib
import datetime


def grabImage(file=None):
    if file:
        image = Image.open(file)
        output_buffer = io.BytesIO()
        image.save(output_buffer, format='JPEG')
        return output_buffer.getvalue()
    else:
        # 获取并保存图片 直接从必应上获取
        rsp = httpx.get("https://cn.bing.com/")
        bs = BS(rsp.content, "html.parser")
        bglink = bs.find("link").get("href")
        url = str(rsp.url) + bglink

        image = httpx.get(url).content
        return image

def isINeed(image):
    # # 压缩图片
    img = Image.open(io.BytesIO(image))
    x, y = img.size
    x_s = round(x/2)
    y_s = int(y * x_s / x)
    out = img.resize((x_s, y_s), Image.ANTIALIAS)

    # 图片转码
    output_buffer = io.BytesIO()
    out.save(output_buffer, format='JPEG')
    out.save(r"D:\abc.jpg")
    byte_data = output_buffer.getvalue()
    # 图片识别
    result =  bd.imageRecognition(byte_data)
    print("result:", result)
    # 结果分析

    ## 计算特征
    keywords = ['植物', '树', '天空', '阳光','霞光', '晚霞','海洋','大海','森林','湖泊','草原','沙漠','高山','瀑布']
    score = 0
    for r in result:
        # 进行对比
        for k in keywords:
            root = r.get('keyword', '')
            ratio = difflib.SequenceMatcher(None, root, k).ratio()
            mscore = r.get('score')
            score += mscore*ratio
            print("  text:%s\t vs kwd:%s\tmscore:%f\tratio:%f\tresult:%f" % (root, k, mscore, ratio, mscore*ratio))
    return score

def run(test=False):
    filename = None
    if test:
        filename = r'C:\Users\alisx\Pictures\Saved Pictures\1032781.jpg'
        
    image = grabImage(filename)
    score = isINeed(image)
    if score > 0.5:
        with open(r"C:\Users\alisx\Pictures\Saved Pictures\bing_%s.jpg" % datetime.date.today(), 'wb') as f:
            f.write(image)

if __name__ == '__main__':
    run()

