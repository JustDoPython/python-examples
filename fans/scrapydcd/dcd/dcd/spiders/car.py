import scrapy
from lxml import etree
from dcd.items import DcdItem
import os,csv

if os.path.exists('D:/桌面/car.csv'):
    print('delete?')
    os.remove('D:/桌面/car.csv')
f = open('D:/桌面/car.csv', 'a+', newline='', encoding='gb18030')
f_csv = csv.writer(f)
f_csv.writerow(['品牌','车型', '评分', '特点'])
class RainSpider(scrapy.Spider):
    name = 'car'
    allowed_domains = ['https://www.dongchedi.com/']
    #url中的73代表吉利，18是奇瑞，35是长安，对这3个品牌发起请求
    start_urls = ['https://www.dongchedi.com/auto/library/x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-73-x-x','https://www.dongchedi.com/auto/library/x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-18-x-x','https://www.dongchedi.com/auto/library/x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-35-x-x']

    def parse(self, response):
        print('html111')
        html =etree.HTML(response.text)

        item = DcdItem()
        brand = html.xpath('//*[@id="__next"]/div[1]/div[2]/div/div[4]/span[2]/div/div/a/text()')[0]
        lis = html.xpath('//*[@id="__next"]/div[1]/div[2]/div/ul/li[position()>= 1]')
        print('111 lis',lis)
        for li in lis:
            name = li.xpath('./div/a[1]/text()')[0]
            try:
                #有评分
                score = li.xpath('./div/a[2]/text()')[0].split('分')[0]
            except Exception as e:
                #无评分
                score = 0
            try:
                #有标题
                title = li.xpath('./div/span/text()')[0]
                # print('title111',title)
            except Exception as e:
                #无标题
                title = '无'
            print(name,score,title)
            f_csv.writerow([brand,name,score,title])

        item['name'] = name
        item['score'] = score
        item['title'] = title
        yield item
