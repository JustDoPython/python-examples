#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
from urllib.request import quote
import requests
import random
import traceback
import time
import datetime
import math
import json
import pymysql

from stock import dateUtil


class report:

    def __init__(self):
        self.header = {"Connection": "keep-alive",
                       "Cookie": "st_si=30608909553535; cowminicookie=true; st_asi=delete; cowCookie=true; intellpositionL=2048px; qgqp_b_id=c941d206e54fae32beffafbef56cc4c0; st_pvi=19950313383421; st_sp=2020-10-19%2020%3A19%3A47; st_inirUrl=http%3A%2F%2Fdata.eastmoney.com%2Fstock%2Flhb.html; st_sn=15; st_psi=20201026225423471-113300303752-5813912186; intellpositionT=2579px",
                          "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
                          "Host": "reportapi.eastmoney.com"
                          }

        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='east_money', charset='utf8')
        self.cur = self.conn.cursor()
        self.url = 'http://reportapi.eastmoney.com/report/list?cb=datatable1351846&industryCode=*&pageSize={}&industry=*&rating=&ratingChange=&beginTime={}&endTime={}&pageNo={}&fields=&qType=0&orgCode=&code=*&rcode=&p=2&pageNum=2&_=1603724062679'

    def getHtml(self, pageSize, beginTime, endTime, pageNo):
        print(self.url.format(pageSize, beginTime, endTime, pageNo))
        response = requests.get(self.url.format(pageSize, beginTime, endTime, pageNo), headers=self.header)
        html = response.content.decode("utf-8")

        return html

    def format_content(self, content):
        if len(content):
            content = content.replace('datatable1351846(', '')[:-1]
            return json.loads(content)
        else:
            return None


    def parse_data(self, items):
        result_list = []
        for i in items['data']:
            result = {}
            obj = i
            result['title'] = obj['title'] #报告名称
            result['stockName'] = obj['stockName'] #股票名称
            result['stockCode'] = obj['stockCode'] #股票code
            result['orgCode'] = obj['stockCode'] #机构code
            result['orgName'] = obj['orgName'] #机构名称
            result['orgSName'] = obj['orgSName'] #机构简称
            result['publishDate'] = obj['publishDate'] #发布日期
            result['predictNextTwoYearEps'] = obj['predictNextTwoYearEps'] #后年每股盈利
            result['predictNextTwoYearPe'] = obj['predictNextTwoYearPe'] #后年市盈率
            result['predictNextYearEps'] = obj['predictNextYearEps'] # 明年每股盈利
            result['predictNextYearPe'] = obj['predictNextYearPe'] # 明年市盈率
            result['predictThisYearEps'] = obj['predictThisYearEps'] #今年每股盈利
            result['predictThisYearPe'] = obj['predictThisYearPe'] #今年市盈率
            result['indvInduCode'] = obj['indvInduCode'] # 行业代码
            result['indvInduName'] = obj['indvInduName'] # 行业名称
            result['lastEmRatingName'] = obj['lastEmRatingName'] # 上次评级名称
            result['lastEmRatingValue'] = obj['lastEmRatingValue'] # 上次评级代码
            result['emRatingValue'] = obj['emRatingValue'] # 评级代码
            result['emRatingName'] = obj['emRatingName'] # 评级名称
            result['ratingChange'] = obj['ratingChange'] # 评级变动
            result['researcher'] = obj['researcher'] # 研究员
            result['encodeUrl'] = obj['encodeUrl'] # 链接
            result['count'] = int(obj['count']) # 近一月个股研报数

            result_list.append(result)

        return result_list


    def get_data(self, start_date, end_date):
        html = self.getHtml(100, start_date, end_date, 1)
        content_json = self.format_content(html)
        page_num = content_json['TotalPage']
        print(page_num)

        data_list = []
        for i in range(1, page_num + 1):
            ihtml = self.getHtml(100, start_date, end_date, i)
            icontent_json = self.format_content(ihtml)
            result_list = self.parse_data(icontent_json)
            data_list.extend(result_list)

            time.sleep(random.randint(1, 4))
        return data_list

    def deal(self, start_date, end_date):
        data_list = self.get_data(start_date, end_date)
        if data_list and data_list is not None:
            self.insertdb(data_list)

        self.cur.close()
        self.conn.close()

    def insertdb(self, data_list):
        attrs = ['title', 'stockName', 'stockCode', 'orgCode', 'orgName', 'orgSName', 'publishDate', 'predictNextTwoYearEps',
                 'predictNextTwoYearPe', 'predictNextYearEps', 'predictNextYearPe', 'predictThisYearEps', 'predictThisYearPe',
                 'indvInduCode', 'indvInduName', 'lastEmRatingName', 'lastEmRatingValue', 'emRatingValue',
                 'emRatingName', 'ratingChange', 'researcher', 'encodeUrl', 'count']
        insert_tuple = []
        for obj in data_list:
            insert_tuple.append((obj['title'], obj['stockName'], obj['stockCode'], obj['orgCode'], obj['orgName'], obj['orgSName'], obj['publishDate'], obj['predictNextTwoYearEps'], obj['predictNextTwoYearPe'], obj['predictNextYearEps'], obj['predictNextYearPe'], obj['predictThisYearEps'], obj['predictThisYearPe'], obj['indvInduCode'], obj['indvInduName'], obj['lastEmRatingName'], obj['lastEmRatingValue'], obj['emRatingValue'],obj['emRatingName'], obj['ratingChange'], obj['researcher'], obj['encodeUrl'], obj['count']))
        values_sql = ['%s' for v in attrs]
        attrs_sql = '('+','.join(attrs)+')'
        values_sql = ' values('+','.join(values_sql)+')'
        sql = 'insert into %s' % 'report'
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


if __name__ == "__main__":
    report = report()
    today = dateUtil.DateUtil.get_today()
    one_year_before = dateUtil.DateUtil.get_format_day(dateUtil.DateUtil.get_minus_time(datetime.datetime.now(), days=365), '%Y-%m-%d')
    report.deal(one_year_before, today)
