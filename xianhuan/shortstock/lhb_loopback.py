#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""

from common import config
from common import stock_utils
from db import MysqldbHelper
from ana import lhb_history_pick
import pyecharts.options as opts
from pyecharts.charts import Line, Page
import pandas as pd

class LhbLoopback:

    mdb = MysqldbHelper.MysqldbHelper(config.mysql_config)
    mdb.selectDataBase('east_money')

    def query_stock_detail(self, scode, day):
        query_sql = "SELECT * FROM stock_day_info WHERE CODE='%s' AND DAY>='%s' ORDER BY DAY asc LIMIT 4" % (scode, day)
        return self.mdb.diy_query(query_sql)

    def query_date(self, day):
        query_sql = "SELECT DISTINCT tdate FROM lhb_stock_stat WHERE tdate>'%s' and tdate<'%s' ORDER BY tdate asc limit 100" % (day, '2019-06-30')
        return self.mdb.diy_query(query_sql)

    def draw_pic(self, x_data, y_data1, y_data2, y_data3):
        # 处理数据
        yd1 = ["%.2f" % (x*100) for x in y_data1]
        yd2 = ["%.2f" % (x*100) for x in y_data2]
        yd3 = ["%.2f" % (x*100) for x in y_data3]

        # 人口结构折线图
        line = Line(init_opts=opts.InitOpts(width='1600px', height='500px'))
        line.add_xaxis(x_data)
        line.add_yaxis('乐观上涨点数', yd1, label_opts=opts.LabelOpts(is_show=False))
        line.add_yaxis('平均上涨点数', yd2, label_opts=opts.LabelOpts(is_show=False))
        line.add_yaxis('悲观上涨点数', yd3, label_opts=opts.LabelOpts(is_show=False))
        line.set_global_opts(
            title_opts=opts.TitleOpts(title="短线操作收益", pos_bottom="bottom", pos_left="center"),
            xaxis_opts=opts.AxisOpts(
                name='日期',
                name_location='end',
                type_="category",
                # axislabel_opts=opts.LabelOpts(is_show=True, color="#000", interval=0, rotate=90),
                axistick_opts=opts.AxisTickOpts(is_show=True, is_align_with_label=True),
                axispointer_opts=opts.AxisPointerOpts(type_="shadow", label=opts.LabelOpts(is_show=True))
            ),
            # y轴相关选项设置
            yaxis_opts=opts.AxisOpts(
                name='收益点数',
                type_="value",
                position="left",
                axislabel_opts=opts.LabelOpts(is_show=True)
            ),
            legend_opts=opts.LegendOpts(is_show=True)
        )

        # 渲染图像，将多个图像显示在一个html中
        # DraggablePageLayout表示可拖拽
        page = Page(layout=Page.DraggablePageLayout)
        page.add(line)
        page.render('up.html')

    def compute(self, date, stat_type):
        ### stat_type 表示统计类型，1-计算两天，2-计算三天 ###
        # 1. 获取每日的龙虎榜选股(根据概率倒序)
        lhbpick = lhb_history_pick.lhbHisPick()
        pick_list = lhbpick.deal(date)

        if pick_list is None or not len(pick_list):
            return None, None, None

        # 2. 根据选股计算上涨点数
        for stock in pick_list:
            # 将退市警示股和新股排除
            if 'ST' in stock['name'] or '*ST' in stock['name'] or 'N' in stock['name']:
                continue

            # 获取股票三日行情数据
            stock_day_detail = self.query_stock_detail(stock['scode'], date)
            # 选股当天收盘价
            day_close_price = stock_day_detail[0]['close_price']
            # 选股后一天涨停价
            first_day_limit = stock_utils.StockUtils.calc_limit_price(day_close_price)
            # 选股后一天最低价
            first_day_low_price = stock_day_detail[1]['low_price']
            # 选股后一天最高价
            first_day_top_price = stock_day_detail[1]['top_price']
            # 选股后一天开盘价
            first_day_open = stock_day_detail[1]['open_price']
            # 选股后一天平均价
            first_day_avg_price = (first_day_top_price + first_day_low_price) / 2
            # 开盘即涨停并且一天未开板，买不进，放弃
            if first_day_low_price == first_day_top_price or first_day_limit == first_day_open:
                continue

            # 选股后二天最低价
            second_day_low_price = stock_day_detail[2]['low_price']
            # 选股后二天最高价
            second_day_top_price = stock_day_detail[2]['top_price']
            # 选股后二天平均价
            second_day_avg_price = (second_day_top_price + second_day_low_price) / 2

            # 计算上榜后两天的情况
            optim_up2 = (second_day_top_price - first_day_low_price) / first_day_low_price
            pessim_up2 = (second_day_low_price - first_day_top_price) / first_day_top_price
            avg_up2 = (second_day_avg_price - first_day_avg_price) / first_day_avg_price

            if stat_type == 1:
                # print(optim_up2, pessim_up2, avg_up2)
                return optim_up2, pessim_up2, avg_up2

            # 选股后三天最低价
            third_day_low_price = stock_day_detail[3]['low_price']
            # 选股后三天最高价
            third_day_top_price = stock_day_detail[3]['top_price']
            # 选股后三天平均价
            third_day_avg_price = (second_day_top_price + second_day_low_price) / 2

            # 计算上榜后三天的情况
            max2 = max(first_day_top_price, second_day_top_price)
            min2 = min(first_day_low_price, second_day_low_price)
            avg2 = (first_day_avg_price + second_day_avg_price) / 2

            optim_up3 = (third_day_top_price - min2) / min2
            pessim_up3 = (third_day_low_price - max2) / max2
            avg_up3 = (third_day_avg_price - avg2) / avg2

            return optim_up3, pessim_up3, avg_up3

        return None, None, None

    def deal_optim_days(self):
        optim_days = self.query_date('2019-02-01')

        result_list = []
        for day in optim_days:
            optim_up, pessim_up, avg_up = self.compute(day['tdate'], 1)
            result_list.append({'optim': optim_up if optim_up is not None else 0, 'pessim': pessim_up if pessim_up is not None else 0, 'avg': avg_up if avg_up is not None else 0})

        x_data = pd.DataFrame(optim_days)
        ydata = pd.DataFrame(result_list)
        self.draw_pic(x_data['tdate'], ydata['optim'], ydata['avg'], ydata['pessim'])
        print(result_list)

    def deal_shake_days(self):
        shake_days = self.query_date('2019-03-19')

        result_list = []
        for day in shake_days:
            optim_up, pessim_up, avg_up = self.compute(day['tdate'], 2)
            result_list.append({'optim': optim_up if optim_up is not None else 0, 'pessim': pessim_up if pessim_up is not None else 0, 'avg': avg_up if avg_up is not None else 0})

        x_data = pd.DataFrame(shake_days)
        ydata = pd.DataFrame(result_list)
        self.draw_pic(x_data['tdate'], ydata['optim'], ydata['avg'], ydata['pessim'])
        print(result_list)

    def deal_pessim_days(self):
        pessim_days = self.query_date('2019-04-23')

        result_list = []
        for day in pessim_days:
            optim_up, pessim_up, avg_up = self.compute(day['tdate'], 2)
            result_list.append({'optim': optim_up if optim_up is not None else 0, 'pessim': pessim_up if pessim_up is not None else 0, 'avg': avg_up if avg_up is not None else 0})

        x_data = pd.DataFrame(pessim_days)
        ydata = pd.DataFrame(result_list)
        self.draw_pic(x_data['tdate'], ydata['optim'], ydata['avg'], ydata['pessim'])
        print(result_list)

if __name__ == '__main__':
    lhb = LhbLoopback()
    # lhb.deal_optim_days()
    # lhb.deal_pessim_days()
    lhb.deal_shake_days()


