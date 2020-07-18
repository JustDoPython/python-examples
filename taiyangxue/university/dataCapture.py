import requests as rq
from bs4 import BeautifulSoup as Bs
from bs4.element import Tag
import pandas as pd
import numpy as np
import openpyxl
def getData(resLoc):
    rp = rq.get(resLoc)
    rp.encoding = 'utf-8'
    return rp.text

def dataProcessing(html, num):
    rows = Bs(html, 'html.parser').table.find_all('tr', limit=num, recursive=True)

    thf = []
    for th in rows[0].find_all('th', limit=10):
        if th.text.find('\r\n') == -1 and th.text.find('\n') == -1:
            thf.append(th.contents)
    for i in [op.contents for op in rows[0].find_all('option', recursive=True)]:
        thf.append(i)
    thf = ["".join(th) for th in thf]

    universityList = []
    for tr in rows[1:]:
        tds = tr.find_all('td')
        if len(tds) == 0:
            continue
        contents = [td.contents for td in tds]
        if len(contents[0]) > 1:
            contents[0] = [contents[0][0]]
        contents[1] = contents[1][0].contents
        universityList.append(["".join(attr) for attr in contents])

    return pd.DataFrame(np.array(universityList), columns=thf)

def dataProcessing2015(html, num):
    rows = Bs(html, 'html.parser').table.find_all('tr', limit=num, recursive=True)

    universityList = []
    thf = []
    for tr in rows[1:]:
        tds = tr.find_all('td')
        if len(tds) == 0:
            continue
        contents = [td.contents for td in tds]
        if len(contents[0]) > 1:
            contents[0] = [contents[0][0]]
        contents[1] = contents[1][0].contents
        universityList.append("".join(attr) for attr in contents)
        
    for th in rows[0].find_all('th', limit=10):
        if th.text.find('\r\n') == -1 and th.text.find('\n') == -1:
            thf.append(th.contents)
    for th in rows[1].find_all('th', limit=10):
        thf.append(th.contents)

    thft = []
    for th in thf:
        title = []
        for t in th:
            if type(t) == Tag:   # 对含有 html 标签的标题进行处理
                title.append(t.text)
            else:
                title.append(t)
        thft.append("".join(title))

    thf = thft
    univList = []
    for university in universityList:
        university = ["".join(attr) for attr in university]
        univList.append(university)
    return pd.DataFrame(np.array(univList), columns=thf)

def saveData(data, year, index=None):
    if index:
        data.to_excel('university_%d_%d.xlsx' % (year,index), index=False)
    else:
        data.to_excel('university_%d.xlsx' % year, index=False)

def main(num, year, index=None):
    if num >= 550:
        return
    else:
        if year == 2015:
            url = 'http://zuihaodaxue.com/zuihaodaxuepaiming%d_%d.html' % (year, index)
            saveData(dataProcessing2015(getData(url), num + 1), year, index)
        else:
            url = 'http://zuihaodaxue.com/zuihaodaxuepaiming%d.html' % year
            saveData(dataProcessing(getData(url), num + 1), year)
def download2015(num):
    # for i in range(1,4): # 2015年
    #     print(i)
    #     main(num, 2015, i)
    df = None
    for i in range(1,4):
        url = 'http://zuihaodaxue.com/zuihaodaxuepaiming%d_%d.html' % (2015, i)
        dft = dataProcessing2015(getData(url), num + 1)
        if df is None:
            df = dft
        else:
            df = pd.merge(df, dft)
    saveData(df, 2015)


# 测试,爬取所有 名大学的信息
for i in range(2015,2020):
    print(i)
    if i == 2015:
        download2015(549)
    else:
        main(549, i)

#————————————————
#版权声明：本文为CSDN博主「硕子鸽」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
#原文链接：https://blog.csdn.net/weixin_43941364/java/article/details/105949701