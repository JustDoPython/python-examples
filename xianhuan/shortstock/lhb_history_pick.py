#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""

from common import config
from common import dateUtil
from common import dingtalkUtil
from db import MysqldbHelper


class lhbHisPick:

    mdb = MysqldbHelper.MysqldbHelper(config.mysql_config)
    mdb.selectDataBase('east_money')

    # 查询一天的龙虎榜详情
    def query_one_day_detail(self, day):
        query_sql = "SELECT tdate,scode,sales_code,sales_name, buy_money,sell_money,net_money,his_rank_rate " \
                    "FROM lhb_stock_detail WHERE 1=1 and type=0 and tdate= '%s'" % day
        print(query_sql)
        return self.mdb.diy_query(query_sql)

    def query_code_name(self, scode, day):
        query_sql = "SELECT NAME FROM stock_day_info WHERE 1=1 AND CODE='%s' and DAY='%s'" % (scode, day)
        return self.mdb.diy_query(query_sql)

    def query_yyb_rank(self, day, yyb):
        query_sql = "SELECT * FROM yyb_stat WHERE ctype=3 AND update_date='%s' AND sales_name='%s'" % (day, yyb)
        return self.mdb.diy_query(query_sql)

    def quchong(self, detail_list):
        undup_detail_list = []
        if detail_list is not None and len(detail_list):
            for item in detail_list:
                if item not in undup_detail_list:
                    undup_detail_list.append(item)
        return undup_detail_list

    def ana(self, detail_list):
        scode_dict = {}
        rank_list = []
        for detail in detail_list:
            if detail['scode'] not in scode_dict.keys():
                sub_list = [detail]
                scode_dict[detail['scode']] = sub_list
            else:
                sub_list = scode_dict[detail['scode']]
                sub_list.append(detail)
                scode_dict[detail['scode']] = sub_list

        for key in scode_dict.keys():
            scode = key
            sub_list = scode_dict[key]
            # 总买入额
            total_money = float(0)
            # 营业部上涨概率
            yyb_avg_rate_list = []
            for detail in sub_list:
                total_money = total_money + float(detail['buy_money'])
                yyb_avg_rate_list.append(float(detail['his_rank_rate']))

            # 买入额占比
            money_rate_list = [float(item['buy_money'])/total_money for item in sub_list]
            total_rate = float(0)
            for i in range(0, len(sub_list)):
                total_rate = float(total_rate) + float(yyb_avg_rate_list[i] * money_rate_list[i])
            rank_list.append({'scode': scode, 'total_rate': total_rate})

        rank_list.sort(key=lambda it: it.get('total_rate'), reverse=True)
        return rank_list

    def deal(self, day):
        if day is None:
            day = dateUtil.DateUtil.get_today()
        detail_list = self.query_one_day_detail(day)
        if detail_list is not None and len(detail_list):
            undup_detail_list = self.quchong(detail_list)
            rank_list = self.ana(undup_detail_list)
            result_list = []
            for rank in rank_list:
                if float(rank['total_rate']) > 50:
                    name = self.query_code_name(rank['scode'], day)
                    if name is not None and len(name):
                        rank['name'] = name[0]['NAME']
                        result_list.append(rank)
            print(result_list)
            return result_list
        return None

if __name__ == '__main__':
    lhbPick = lhbHisPick()
    lhbPick.deal('2020-03-12')