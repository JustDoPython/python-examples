import re
import os
import datetime
from baidu_api import ip2province
import pandas as pd
import openpyxl
from openpyxl import load_workbook

# 命名分组
obj = re.compile(r'(?P<ip>.*?)- - \[(?P<time>.*?)\] "(?P<request>.*?)" (?P<status>.*?) (?P<bytes>.*?) "(?P<referer>.*?)" "(?P<ua>.*?)"')
def load_log(path):
    lst = []
    error_lst = []
    i = 0
    with open(path, mode="r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            dic = parse(line)
            if dic:  # 正确的数据添加到lst列表中
                lst.append(dic)
            else:
                error_lst.append(line)  # 脏数据添加到error_lst列表中
            i += 1
            if i % 1000 == 0:
                print(i,"行")
    return lst, error_lst

def parse(line):
    # 解析单行nginx日志
    dic = {}
    try:
        # print(line)
        result = obj.match(line)
        # print(result.group("time"))
        # ip处理
        ip = result.group("ip")
        if ip.strip() == '-' or ip.strip() == "":  # 如果是匹配到没有ip就把这条数据丢弃
            return False
        dic['ip'] = ip.split(",")[0].strip()  # 如果有两个ip，取第一个ip
        dic['province'] = ip2province(dic['ip'])  # 用 IP 转换为省份
        # print("dic['province']:",dic['province'])
        # 状态码处理
        status = result.group("status")  # 状态码
        dic['status'] = status

        # 时间处理
        time = result.group("time")  # 21/Dec/2019:21:45:31 +0800
        time = time.replace(" +0800", "")  # 替换+0800为空
        t = datetime.datetime.strptime(time, "%d/%b/%Y:%H:%M:%S")  # 将时间格式化成友好的格式
        dic['time'] = t
        dic['hour'] = t.hour
        # request处理
        request = result.group("request")
        a = request.split()[1].split("?")[0]  # 往往url后面会有一些参数，url和参数之间用?分隔，取出不带参数的url
        dic['request'] = a

        # user_agent处理
        ua = result.group("ua")
        if "Windows NT" in ua:
            u = "windows"
        elif "iPad" in ua:
            u = "ipad"
        elif "Android" in ua:
            u = "android"
        elif "Macintosh" in ua:
            u = "mac"
        elif "iPhone" in ua:
            u = "iphone"
        else:
            u = "其他设备"
        dic['ua'] = u

        # refer处理
        referer = result.group("referer")
        dic['referer'] = referer

        return dic
    except Exception as e:
        print("[parse]",line, "-->", e)
        return None

def analyse(lst, datafile):
    df = pd.DataFrame(lst)  # 创建 DataFrame

    # 统计省份
    province_count_df = pd.value_counts(df['province']).reset_index().rename(columns={"index": "province", "province": "count"})

    # 统计时段
    hour_count_df = pd.value_counts(df['hour']).reset_index().rename(columns={"index": "hour", "hour": "count"}).sort_values(by='hour')

    # 统计客户端
    ua_count_df = pd.value_counts(df['ua']).reset_index().rename(columns={"index": "ua", "ua": "count"})

    # 数据存储
    to_excel(province_count_df, datafile, sheet_name='省份')
    to_excel(hour_count_df, datafile, sheet_name='按时')
    to_excel(ua_count_df, datafile, sheet_name='客户端')
    
def to_excel(dataframe, filepath, sheet_name):
    if os.path.exists(filepath):
        excelWriter = pd.ExcelWriter(filepath, engine='openpyxl')
        book = load_workbook(excelWriter.path)
        excelWriter.book = book
        dataframe.to_excel(excel_writer=excelWriter,sheet_name=sheet_name,index=None, header=None)
        excelWriter.close()
    else:
        dataframe.to_excel(filepath, sheet_name=sheet_name, index=None, header=None)

if __name__ == '__main__':
    lst, error_lst = load_log("nginx_access.log")
    analyse(lst, "data.xlsx")