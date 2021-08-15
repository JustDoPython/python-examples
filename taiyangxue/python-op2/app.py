#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/26 14:48
# @Author : way
# @Site :
# @Describe:

import os
import sys

# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from flask import Flask, render_template, jsonify
from datasource.main import  SaleRecord, DBSqlite
from flask import request
# import data as sd
# from .data import SourceData

app = Flask(__name__)

source = {}
datasource = SaleRecord(DBSqlite("datasource/database.db"))

@app.route('/')
@app.route('/check_rate')
def check_rate():
    data = datasource.show_check_rate(rtype='dict')
    ret = [['date', '1组', '2组', '3组', '4组', '5组']]
    for d in data:
        row = []
        for k in d:
            row.append(d[k])
        ret.append(row)
    return render_template('check_rate.html', title='打卡率', data=ret)

# 成员数据
@app.route('/memberdata')
def memberdata():
    return render_template('memberdata.html', title='成员数据')

# 组长数据
@app.route('/teamleader')
def teamleader():
    return render_template('teamleader.html', title='组长数据')

@app.route('/sale')
def sale_page():
    return render_template('sale.html', title='开单数据')

#-------api----------
@app.route('/api/memberdata')
def api_memberdata():
    data = {'data': datasource.show_member_score(rtype='dict')}
    return jsonify(data)

@app.route('/api/teamcheckdetail')
def api_teamcheckdetail():
    date = request.args.getlist('date')[0]
    team = request.args.getlist('team')[0]
    data = {'data': datasource.get_team_check_detail(team= team, date=date)}
    return jsonify(data)

@app.route('/api/teamleader')
def api_teamleader():
    data = {'data': datasource.show_leader_score(rtype='dict')}
    return jsonify(data)

@app.route('/api/sale')
def api_sale():
    data = {'data': datasource.get_sale_data()}
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
    
