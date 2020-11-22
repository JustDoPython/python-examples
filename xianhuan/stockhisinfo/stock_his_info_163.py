#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网易财经股票历史数据下载
@author: 闲欢
"""

import requests
import json
from bs4 import BeautifulSoup
import traceback
import pymysql

class StockHisInfo:

    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='east_money', charset='utf8')
        self.cur = self.conn.cursor()


    def get_data(self, code, year, season):
        url = 'http://quotes.money.163.com/trade/lsjysj_%s.html?year=%s&season=%d' % (code, year, season)
        ua_header = {"Connection": "keep-alive",
                     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
                     "Host": "quotes.money.163.com",
                     "Cookie": "vjuids=2453fea.1759e01b4ef.0.c69c7922974aa; _ntes_nnid=99f0981d725ac03af6da5eec0508354e,1604673713410; _ntes_nuid=99f0981d725ac03af6da5eec0508354e; _ntes_stock_recent_=1300033; _ntes_stock_recent_=1300033; _ntes_stock_recent_=1300033; ne_analysis_trace_id=1604846790608; s_n_f_l_n3=20f075946bacfe111604846790626; _antanalysis_s_id=1604933714338; vjlast=1604673713.1605015317.11; pgr_n_f_l_n3=20f075946bacfe1116050154486829637; vinfo_n_f_l_n3=20f075946bacfe11.1.0.1604846790623.0.1605015456187",
                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                     "Accept-Encoding": "gzip, deflate",
                     "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,fr;q=0.7",
                     "Cache-Control": "no-cache",
                     "Pragma": "no-cache",
                     "Referer": "http://quotes.money.163.com/trade/lsjysj_%s.html" % code,
                     "Upgrade-Insecure-Requests": "1",
                     }
        response = requests.get(url, headers=ua_header, verify=False)
        content = response.content.decode("utf-8")

        return content

    def parse_data(self, code, name, content):
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find("table", class_="table_bg001 border_box limit_sale").prettify()
        tb_soup = BeautifulSoup(table, 'html.parser')
        tr_list = tb_soup.find_all('tr')
        stock_list = []
        if len(tr_list):
            del tr_list[0]
            for tr in tr_list:
                items = tr.text.split('\n\n')
                if len(items):
                    del items[0]
                    stock = {}
                    stock['day'] = items[0].replace('\n ', '').replace(' ', '')
                    stock['code'] = code
                    stock['name'] = name
                    stock['open_price'] = self.trans_float(items[1].replace('\n ', '').replace(' ', ''))
                    stock['top_price'] = self.trans_float(items[2].replace('\n ', '').replace(' ', ''))
                    stock['low_price'] = self.trans_float(items[3].replace('\n ', '').replace(' ', ''))
                    stock['close_price'] = self.trans_float(items[4].replace('\n ', '').replace(' ', ''))
                    # stock['last_price'] = self.trans_float(items[7])
                    stock['add_point'] = self.trans_float(items[5].replace('\n ', '').replace(' ', ''))
                    stock['add_percent'] = self.trans_float(items[6].replace('\n ', '').replace(' ', ''))
                    stock['volumn'] = self.trans_float(items[7].replace('\n ', '').replace(' ', '').replace(',', ''))
                    stock['turnover'] = self.trans_float(items[8].replace('\n ', '').replace(' ', '').replace(',', ''))
                    stock['amplitude'] = self.trans_float(items[9].replace('\n ', '').replace(' ', ''))
                    stock['exchange_rate'] = self.trans_float(items[10].replace('\n \n', '').replace(' ', ''))
                    # stock['market_value'] = self.trans_float(items[13])
                    # stock['flow_market_value'] = self.trans_float(items[14])

                    stock_list.append(stock)

        return stock_list

    def query_lcode(self, day):
        query_sql = "select code,name from stock_info where day='%s'" % day

        try:
            lcode = self.cur.execute_sql(query_sql)
            return lcode
        except Exception:
            #输出异常信息
            traceback.print_exc()

    def insertdb(self, data_list):
        attrs = ['day', 'code', 'name', 'open_price', 'top_price', 'low_price', 'close_price', 'add_point',
                 'add_percent', 'volumn', 'turnover', 'amplitude', 'exchange_rate']
        insert_tuple = []
        for obj in data_list:
            insert_tuple.append((obj['day'], obj['code'], obj['name'], obj['open_price'], obj['top_price'], obj['low_price'], obj['close_price'], obj['add_point'], obj['add_percent'], obj['volumn'], obj['turnover'], obj['amplitude'], obj['exchange_rate']))
        values_sql = ['%s' for v in attrs]
        attrs_sql = '('+','.join(attrs)+')'
        values_sql = ' values('+','.join(values_sql)+')'
        sql = 'insert into %s' % 'stock_info'
        sql = sql + attrs_sql + values_sql
        try:
            print(sql)
            for i in range(0, len(insert_tuple), 20000):
                self.cur.executemany(sql, tuple(insert_tuple[i:i+20000]))
                self.conn.commit()
        except pymysql.Error as e:
            self.conn.rollback()
            error = 'insertMany executemany failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            print(error)


    @staticmethod
    def trans_float(s):
        try:
            return float(s)
        except Exception:
            return 0.00

    def deal(self, day, year, season):
        lcode = self.query_lcode(day)
        for code,name in lcode:
            content = self.get_data(code, year, season)
            stock_list = self.parse_data(code, name, content)
            if len(stock_list):
                self.insertdb(stock_list)


if __name__ == "__main__":
    sdi = StockHisInfo()
    sdi.deal('2020-11-11', '2020', 3)
