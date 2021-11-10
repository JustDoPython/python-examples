#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
from lxml import etree

text = '''
<div>
            <ul id='ultest'>
                 <li class="item-0"><a href="link1.html">first item</a></li>
                 <li class="item-1"><a href="link2.html">second item</a></li>
                 <li class="item-inactive"><a href="link3.html">third item</a></li>
                 <li class="item-1"><a href="link4.html"><span>fourth item</span></a></li>
                 <li class="item-0"><a href="link5.html">fifth item</a> # 注意，此处缺少一个 </li> 闭合标签
             </ul>
         </div>
'''

# 调用HTML类进行初始化，这样就成功构造了一个XPath解析对象。
page = etree.HTML(text)
print(type(page))
print(etree.tostring(page))

# nodename
print(page.xpath("ul"))

# /
print(page.xpath("/html"))

# //
print(page.xpath("//li"))

# .
ul = page.xpath("//ul")
print(ul)
print(ul[0].xpath("."))
print(ul[0].xpath("./li"))

# ..
print(ul[0].xpath(".."))

# @
print(ul[0].xpath("@id"))

# 谓语
# 第三个li标签
print(page.xpath('//ul/li[3]'))
# 最后一个li标签
print(page.xpath('//ul/li[last()]'))
# 倒数第二个li标签
print(page.xpath('//ul/li[last()-1]'))
# 序号小于3的li标签
print(page.xpath('//ul/li[position()<3]'))
# 有class属性的li标签
print(page.xpath('//li[@class]'))
# class属性为item-inactive的li标签
print(page.xpath("//li[@class='item-inactive']"))


# 获取文本
# text()
print(page.xpath('//ul/li/a/text()'))
# string()
print(page.xpath('string(//ul)'))

# 通配符
print(page.xpath('//li/*'))
print(page.xpath('//li/@*'))

# |
print(page.xpath("//li|//a"))

# 函数
# contains
print(page.xpath("//*[contains(@class, 'item-inactive')]"))

# starts-with
print(page.xpath("//*[starts-with(@class, 'item-inactive')]"))


# 节点轴
# ancestor轴
print(page.xpath('//li[1]/ancestor::*'))
# attribute轴
print(page.xpath('//li[1]/attribute::*'))
# child轴
print(page.xpath('//li[1]/child::a[@href="link1.html"]'))
# descendant轴
print(page.xpath('//li[4]/descendant::span'))
# following轴
print(page.xpath('//li[4]/following::*[2]'))
# following-sibling轴
print(page.xpath('//li[4]/following-sibling::*'))


