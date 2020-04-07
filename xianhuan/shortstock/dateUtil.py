#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
import datetime
import pandas as pd


class DateUtil:

    @staticmethod
    def get_format_time(basetime, dformat='%Y-%m-%d %H:%M:%S'):
        return datetime.datetime.strftime(basetime, dformat)

    @staticmethod
    def get_format_day(basetime, dformat='%Y-%m-%d'):
        return datetime.datetime.strftime(basetime, dformat)
    
    @staticmethod
    def get_today(dformat='%Y-%m-%d'):
        return datetime.datetime.now().strftime(dformat)

    @staticmethod
    def get_now(dformat='%Y-%m-%d %H:%M:%S'):
        return datetime.datetime.now().strftime(dformat)

    @staticmethod
    def get_year():
        return datetime.datetime.now().strftime('%Y')

    @staticmethod
    def get_month():
        return datetime.datetime.now().strftime('%m')

    @staticmethod
    def get_day():
        return datetime.datetime.now().strftime('%d')

    @staticmethod
    def get_delt_days(starttime, endtime):
        return (endtime - starttime).days

    @staticmethod
    def get_delt_secs(starttime, endtime):
        return (endtime - starttime).microseconds

    @staticmethod
    def get_add_time(basetime, days=0, hours=0, minutes=0, seconds=0):
        return basetime + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    @staticmethod
    def get_minus_time(basetime, days=0, hours=0, minutes=0, seconds=0):
        return basetime - datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    @staticmethod
    def get_date_list(startdate, enddate, freq='1D', dformat='%Y-%m-%d'):
        tm_rng = pd.date_range(startdate, enddate, freq=freq)
        return [x.strftime(dformat) for x in tm_rng]


if __name__ == '__main__':
    util = DateUtil()
    print(DateUtil.get_today('%Y/%m/%d'))
    print(DateUtil.get_now())
    print(DateUtil.get_year())
    print(DateUtil.get_month())
    print(DateUtil.get_day())
    print(DateUtil.get_delt_secs(datetime.datetime(2020,10,1), datetime.datetime.now()))
    print(DateUtil.get_add_time(datetime.datetime.now(), days=10, hours=2))
    print(DateUtil.get_minus_time(datetime.datetime.now(), days=10, hours=2))
    print(DateUtil.get_format_time(basetime=DateUtil.get_minus_time(datetime.datetime.now(), days=10, hours=2)))
    print(DateUtil.get_date_list(startdate='2020-02-02', enddate='2020-02-03'))
