# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DcdItem(scrapy.Item):
    #品牌
    brand = scrapy.Field()
    #车型
    name = scrapy.Field()
    #评分
    score = scrapy.Field()
    #特点
    title = scrapy.Field()
