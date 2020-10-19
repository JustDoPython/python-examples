# -*- coding: UTF-8 -*-
import json
import re
import sqlite3
import threading
import time

import schedule

import requests
from bs4 import BeautifulSoup
import pyecharts.options as opts
from pyecharts.charts import Line



def insert(data):
    conn = sqlite3.connect('price.db')
    c = conn.cursor()
    sql = 'INSERT INTO price (sku_id,sku_name,price) VALUES ("{}", "{}", "{}")'.format(data.get("sku_id"), data.get("sku_name"), data.get('price') )
    c.execute(sql)
    conn.commit()
    conn.close()

def select(sku_id):
    conn = sqlite3.connect('price.db')
    c = conn.cursor()
    sql = 'select sku_id, sku_name, price, time from price where sku_id = "{}" order by time asc'.format(sku_id)
    cursor = c.execute(sql)

    datas = []
    for row in cursor:
        data = {
            'sku_id': row[0],
            'sku_name': row[1],
            'price': row[2],
            'time': row[3]
        }
        datas.append(data)
    conn.close()

    return datas




def get_jd_price(skuId):

    sku_detail_url = 'http://item.jd.com/{}.html'
    sku_price_url = 'https://p.3.cn/prices/get?type=1&skuid=J_{}'

    r = requests.get(sku_detail_url.format(skuId)).content

    soup = BeautifulSoup(r, 'html.parser', from_encoding='utf-8')
    sku_name_div = soup.find('div', class_="sku-name")

    if not sku_name_div:
        print('您输入的商品ID有误！')
        return
    else:
        sku_name = sku_name_div.text.strip()

    r = requests.get(sku_price_url.format(skuId))
    price = json.loads(r.text)[0]['p']

    data = {
        'sku_id': skuId,
        'sku_name': sku_name,
        'price': price
    }

    insert(data)

def run_price_job(skuId):

    # 使用不占主线程的方式启动 计划任务
    def run_continuously(interval=1):
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    schedule.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run

    # 每天10点运行
    schedule.every().day.at("00:41").do(get_jd_price, skuId=skuId)
    run_continuously()

def line(datas):
    x_data = []
    y_data = []
    for data in datas:
        x_data.append(data.get('time'))
        y_data.append(data.get('price'))

    (
        Line()
        .add_xaxis(x_data)
        .add_yaxis(datas[0].get('sku_name'), y_data, is_connect_nones=True)
        .render("商品历史价格.html")
    )



if __name__ == '__main__':

    skuId = input('请输入商品ID：')

    run_price_job(skuId)
    datas = select(skuId)
    line(datas)