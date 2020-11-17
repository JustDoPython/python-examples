#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

网页财经每日行情排行榜，copy所有股票当日数据

@author: 闲欢
"""

import math

import requests
import json
import traceback
import pymysql



class StockDayInfo:

    def __init__(self):
        self.ua_header = {"Connection": "keep-alive",
                         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
                         "Host": "quotes.money.163.com",
                         "Cookie": "vjuids=2453fea.1759e01b4ef.0.c69c7922974aa; _ntes_nnid=99f0981d725ac03af6da5eec0508354e,1604673713410; _ntes_nuid=99f0981d725ac03af6da5eec0508354e; _ntes_stock_recent_=1300033; ne_analysis_trace_id=1604846790608; s_n_f_l_n3=20f075946bacfe111604846790626; _antanalysis_s_id=1604933714338; vjlast=1604673713.1605426311.11; pgr_n_f_l_n3=20f075946bacfe1116055330765687243; vinfo_n_f_l_n3=20f075946bacfe11.1.0.1604846790623.0.1605533081941"
                         }
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='east_money', charset='utf8')
        self.cur = self.conn.cursor()

    def get_data(self, url):
        response = requests.get(url, headers=self.ua_header, verify=False)
        content = response.content.decode('unicode_escape')
        return content

    def parse_data(self, data):
        result_obj = json.loads(data)

        obj = {}
        obj['pagecount'] = result_obj['pagecount']
        obj['time'] = result_obj['time']
        obj['total'] = result_obj['total']
        list_str = result_obj['list']
        stock_list = []
        if list_str:
            data_list = list(list_str)
            for s in data_list:
                # print(s)
                stock = {}
                stock['query_code'] = s['CODE']
                stock['code'] = s['SYMBOL']
                stock['name'] = s['SNAME']
                if 'PRICE' in s.keys():
                    stock['close_price'] = self.trans_float(s['PRICE'])
                else:
                    stock['close_price'] = 0.00
                if 'HIGH' in s.keys():
                    stock['top_price'] = self.trans_float(s['HIGH'])
                else:
                    stock['top_price'] = 0.00
                if 'LOW' in s.keys():
                    stock['low_price'] = self.trans_float(s['LOW'])
                else:
                    stock['low_price'] = 0.00
                if 'OPEN' in s.keys():
                    stock['open_price'] = self.trans_float(s['OPEN'])
                else:
                    stock['open_price'] = 0.00
                if 'YESTCLOSE' in s.keys():
                    stock['last_price'] = self.trans_float(s['YESTCLOSE'])
                else:
                    stock['last_price'] = 0.00
                if 'UPDOWN' in s.keys():
                    stock['add_point'] = self.trans_float(s['UPDOWN'])
                else:
                    stock['add_point'] = 0.00
                if 'PERCENT' in s.keys():
                    stock['add_percent'] = self.trans_float(s['PERCENT'])
                else:
                    stock['add_percent'] = 0.00
                if 'HS' in s.keys():
                    stock['exchange_rate'] = self.trans_float(s['HS'])
                else:
                    stock['exchange_rate'] = 0.00
                if 'VOLUME' in s.keys():
                    stock['volumn'] = self.trans_float(s['VOLUME'])
                else:
                    stock['volumn'] = 0.00
                if 'TURNOVER' in s.keys():
                    stock['turnover'] = self.trans_float(s['TURNOVER'])
                else:
                    stock['turnover'] = 0.00
                if 'TCAP' in s.keys():
                    stock['market_value'] = self.trans_float(s['TCAP'])
                else:
                    stock['market_value'] = 0.00
                if 'MCAP' in s.keys():
                    stock['flow_market_value'] = self.trans_float(s['MCAP'])
                else:
                    stock['flow_market_value'] = 0.00
                stock_list.append(stock)

        obj['stock'] = stock_list

        return obj

    @staticmethod
    def trans_float(s):
        try:
            return float(s)
        except Exception:
            return 0.00

    def insert_db(self, obj_list, day):
        try:
            if len(obj_list):
                insert_attrs = ['day', 'query_code', 'code', 'name', 'close_price', 'top_price', 'low_price', 'open_price', 'last_price', 'add_point', 'add_percent', 'exchange_rate', 'volumn', 'turnover', 'market_value', 'flow_market_value']
                insert_tuple = []
                for obj in obj_list:
                    insert_tuple.append((day,
                                         obj['query_code'],
                                         obj['code'],
                                         obj['name'],
                                         obj['close_price'],
                                         obj['top_price'],
                                         obj['low_price'],
                                         obj['open_price'],
                                         obj['last_price'],
                                         obj['add_point'],
                                         obj['add_percent'],
                                         obj['exchange_rate'],
                                         obj['volumn'],
                                         obj['turnover'],
                                         obj['market_value'],
                                         obj['flow_market_value']))
                values_sql = ['%s' for v in insert_attrs]
                attrs_sql = '('+','.join(insert_attrs)+')'
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
        except Exception:
            #输出异常信息
            traceback.print_exc()


    def deal_json_invaild(self, data):
        data = data.replace("\n", "\\n").replace("\r", "\\r").replace("\n\r", "\\n\\r") \
            .replace("\r\n", "\\r\\n") \
            .replace("\t", "\\t")
        data = data.replace('":"', '&&GSRGSR&&')\
            .replace('":', "%%GSRGSR%%") \
            .replace('","', "$$GSRGSR$$")\
            .replace(',"', "~~GSRGSR~~") \
            .replace('{"', "@@GSRGSR@@") \
            .replace('"}', "**GSRGSR**")
        # print(data)

        data = data.replace('"', r'\"') \
            .replace('&&GSRGSR&&', '":"')\
            .replace('%%GSRGSR%%', '":')\
            .replace('$$GSRGSR$$', '","')\
            .replace("~~GSRGSR~~", ',"')\
            .replace('@@GSRGSR@@', '{"')\
            .replace('**GSRGSR**', '"}')
        # print(data)
        return data

    def deal(self):
        url = 'http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=STYPE%3AEQA&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO.MFRATIO2%2CMFRATIO.MFRATIO10%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=PERCENT&order=desc&count=5000&type=query'
        try:
            content = self.get_data(url)
            print(content)
            obj = self.parse_data(self.deal_json_invaild(content))
            time = obj['time']

            data_list = obj['stock']
            if len(data_list):
                tmp_list = []
                if len(data_list) <= 100:
                    tmp_list = data_list
                else:
                    floor_num = math.floor(len(data_list)/100)
                    for i in range(0, floor_num - 1):
                        insert_list = data_list[100*i:100*(i+1) - 1]
                        self.insert_db(insert_list, time[0:10])
                    tmp_list = data_list[floor_num*100:len(data_list) - 1]

                self.insert_db(tmp_list, time[0:10])
        except Exception as err:
            print(err)
            traceback.print_exc()
            pass


if __name__ == "__main__":
    sdi = StockDayInfo()
    sdi.deal()
    # schedule.every().day.at('16:40').do(sdi.deal())
    # while True:
    #     schedule.run_pending()

