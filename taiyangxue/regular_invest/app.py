import requests as rq
from bs4 import BeautifulSoup as Bs
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
import matplotlib as mpl

# 设置中文字体
mpl.rcParams['font.sans-serif'] = ['KaiTi']
mpl.rcParams['font.serif'] = ['KaiTi']

def fund(code):
    url = 'http://quotes.money.163.com/fund/jzzs_%s_%d.html?start=2001-01-01&end=2020-12-31&sort=TDATE&order=asc'
    # 先获取第一页
    data = pd.DataFrame()
    for i in range(0, 100):
        html = getHtml(url % (code, i))
        page = dataFund(html)
        if page is not None:
            data = data.append(page, ignore_index=True)
        else:
            break
        print("page ", i)
        time.sleep(1)
    filename = 'fund_%s.xlsx' % code
    data.to_excel(filename, index=False)
    print("数据文件:", filename)

def stock(code):
    url = "http://quotes.money.163.com/trade/lsjysj_{code}.html?year={year}&season={season}"

    data = pd.DataFrame()
    for year in range(2001, 2021):
        print('year ', year)
        for season in range(1, 4):
            html = getHtml(url.format(code=code, year=year, season=season))
            page = dataStock(html)
            if page is not None:
                data = data.append(page, ignore_index=True)
    data.sort_values(by='日期')
    filename = 'stock_%s.xlsx' % code
    data.to_excel('stock_%s.xlsx' % code, index=False)
    print("数据文件:", filename)

def getHtml(resLoc):
    while(True):
        rp = rq.get(resLoc)
        rp.encoding = 'utf-8'
        if rp.text.find("对不起!您所访问的页面出现错误") > -1:
            print("获取过于频繁，等待 5 秒再试")
            time.sleep(5)
            continue
        else:
            break
    return rp.text

def dataFund(html):
    table = Bs(html, 'html.parser').table
    if table is None:
        print(html)
        return None
    rows = table.find_all('tr', recursive=True)
    data = []
    columns = [th.text for th in rows[0].find_all('th')]
    for i in range(1, len(rows)):
        data.append(rows[i].text.split('\n')[1:-1])
    if len(data) > 0:
        pdata = pd.DataFrame(np.array(data), columns=columns)
        return pdata
    else:
        return None

def dataStock(html):
    table = Bs(html, 'html.parser').find('table', class_='table_bg001 border_box limit_sale')
    if table is None:
        print(html)
        return None
    rows = table.find_all('tr', recursive=True)
    data = []
    columns = [th.text for th in rows[0].find_all('th')]
    for i in range(1, len(rows)):
        row = [td.text for td in rows[i].find_all('td')]
        data.append(row)
    
    if len(data) > 0:
        data.sort(key=lambda row: row[0])
        pdata = pd.DataFrame(np.array(data), columns=columns)
        return pdata
    else:
        return None

def dataFormat(code, type_='fund', cycleDays=5, begin='2001-01-01'):
    rawdf = pd.read_excel('%s_%s.xlsx' % (type_, code))
    buydf = rawdf[rawdf.index % cycleDays==0] ## 选出定投时机
    # 选择对应的列
    if type_ == 'fund':
        buydf = buydf[['公布日期','单位净值']]
    else:
        buydf = buydf[['日期','收盘价']]
    buydf.columns = ["日期","单价"]

    buydf = buydf[buydf['日期']>=begin]
    return buydf

def show(buydf, amount=1000):
    buydf.insert(2,'定投金额', np.array(len(buydf)*[amount]))  # 增加定投列
    buydf.insert(3,'数量', buydf['单价'].apply(lambda x: amount/x))  # 计算出价值
    buydf.insert(4,'累计本金', buydf['定投金额'].cumsum())  # 计算定投累计
    buydf.insert(5,'累计数量', buydf['数量'].cumsum())  # 计算价值累计
    buydf.insert(6,'当前价值', buydf['累计数量']*buydf['单价']) # 计算实际单价
    # 选取投资比较
    data = pd.DataFrame(columns=['累计本金','当前价值'],
        index=buydf['日期'].to_list(),
        data={'累计本金': buydf['累计本金'].to_list(),
              '当前价值': buydf['当前价值'].to_list()})

    # 净值趋势
    tend = pd.DataFrame(columns=['单价'],index=buydf['日期'].to_list(),data={'单价':buydf['单价'].to_list()})

    tend.plot.line(title="价格走势", linewidth=1, yticks=[])
    plt.show()
    data.plot.line(title="定投效果", linewidth=1, yticks=[])
    plt.show()

if __name__ == "__main__":
    fund("150124")  # 获取数据
    show(dataFormat('150124', begin='2015-05-26'))  # 效果展示
