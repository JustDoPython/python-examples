import json
import datetime
import calendar
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

foundCode = '510300'
file = f'./found_{foundCode}.txt'
found_date_price = {}
found_price_x = []
found_price_y = []

fixed_investment_amount_per_week = 500
fixed_investment_amount_per_month = 2000
my_font = font_manager.FontProperties(fname='/System/Library/Fonts/PingFang.ttc')

with open(file) as f:
    line = f.readline()
    result = json.loads(line)
    for found in result['Data']['LSJZList'][::-1]:
        found_date_price[found['FSRQ']] = found['DWJZ']
        found_price_x.append(found['FSRQ'])
        found_price_y.append(found['DWJZ'])


# 买入规则：从 start_date 日期开始，每逢 weekday 买入，如果 weekday 不是交易日，则顺延至最近的交易日
# 每次买入 500 元，之后转化为相应的份额
def calculate_found_profit_by_week(start_date, end_date, weekday):
    total_stock = 0
    total_amount = 0
    nums = 0
    day = start_date + datetime.timedelta(days=-1)
    while day < end_date:
        day = day + datetime.timedelta(days=1)
        if day.weekday() != weekday:
            continue
        while found_date_price.get(day.strftime('%Y-%m-%d'), None) is None and day < end_date:
            day += datetime.timedelta(days=1)
        if day == end_date:
            break
        nums += 1
        total_stock += round(fixed_investment_amount_per_week / float(found_date_price[day.strftime('%Y-%m-%d')]), 2)
        total_amount += fixed_investment_amount_per_week
        # print(day.strftime('%Y-%m-%d'), found_date_price[day.strftime('%Y-%m-%d')],
        # round(fixed_investment_amount / float(found_date_price[day.strftime('%Y-%m-%d')]), 2), nums)

    # 计算盈利
    while found_date_price.get(end_date.strftime('%Y-%m-%d'), None) is None:
        end_date += datetime.timedelta(days=-1)
    total_profit = round(total_stock, 2) * float(found_date_price[end_date.strftime('%Y-%m-%d')]) - total_amount

    return nums, round(total_stock, 2), total_amount, round(total_profit)


def get_first_day_of_next_month(date):
    first_day = datetime.datetime(date.year, date.month, 1)
    days_num = calendar.monthrange(first_day.year, first_day.month)[1]  # 获取一个月有多少天
    return first_day + datetime.timedelta(days=days_num)


# 买入规则：从 start_date 日期开始，每月 1 号买入，如果 1 号不是交易日，则顺延至最近的交易日
# 每次买入 2000 元，之后转化为相应的份额
def calculate_found_profit_by_month(start_date, end_date):
    total_stock = 0
    total_amount = 0
    nums = 0
    first_day = datetime.datetime(start_date.year, start_date.month, 1)
    day = first_day + datetime.timedelta(days=-1)  # 将日期设置为 start_date 上个月最后一天
    while day < end_date:
        day = get_first_day_of_next_month(day)
        while found_date_price.get(day.strftime('%Y-%m-%d'), None) is None and day < end_date:
            day = day + datetime.timedelta(days=1)
        if day == end_date:
            break
        nums += 1
        total_stock += round(fixed_investment_amount_per_month / float(found_date_price[day.strftime('%Y-%m-%d')]), 2)
        total_amount += fixed_investment_amount_per_month
        # print(day.strftime('%Y-%m-%d'), found_date_price[day.strftime('%Y-%m-%d')],
        # round(fixed_investment_amount / float(found_date_price[day.strftime('%Y-%m-%d')]), 2), nums)

    # 计算盈利
    while found_date_price.get(end_date.strftime('%Y-%m-%d'), None) is None:
        end_date += datetime.timedelta(days=-1)
    total_profit = round(total_stock, 2) * float(found_date_price[end_date.strftime('%Y-%m-%d')]) - total_amount

    return nums, round(total_stock, 2), total_amount, round(total_profit)


start_date = datetime.datetime.fromisoformat('2010-01-01')
end_date = datetime.datetime.fromisoformat('2020-03-01')


def calculate_found_profit_week_month():
    total_amount = []
    total_profit = []

    for i in range(5):
        result = calculate_found_profit_by_week(start_date, end_date, i)
        total_amount.append(result[2])
        total_profit.append(result[3])

    result_month = calculate_found_profit_by_month(start_date, end_date)
    total_amount.append(result_month[2])
    total_profit.append(result_month[3])
    return total_amount, total_profit


total_amount, total_profit = calculate_found_profit_week_month()

print(total_amount)
print(total_profit)

fig, ax = plt.subplots()


## 柱状图
def auto_text(rects):
    for rect in rects:
        ax.text(rect.get_x(), rect.get_height(), rect.get_height(), ha='left', va='bottom')


def show_pic():
    labels = ['周一', '周二', '周三', '周四', '周五', '月定投']
    index = np.arange(len(labels))
    width = 0.2

    fig, ax = plt.subplots()
    rect1 = ax.bar(index - width / 2, total_profit, color='lightcoral', width=width, label='投资收益')
    rect2 = ax.bar(index + width / 2, total_amount, color='springgreen', width=width, label='投资金额')

    plt.title("投入金额 & 收益柱状图", fontproperties=my_font)
    plt.xticks(fontproperties=my_font)
    ax.set_xticks(ticks=index)
    ax.set_xticklabels(labels)

    ax.set_ylim(0, 220000)
    auto_text(rect1)
    auto_text(rect2)

    plt.show()


# show_pic()


# 基金走势
def show_found(found_price_y):
    found_price_y = list(map(float, found_price_y))
    x = [i for i in range(0, len(found_price_y))]

    plt.figure(figsize=(10, 6))

    plt.plot(x, found_price_y, linewidth=1, color='r')

    plt.xlabel('时间', fontproperties=my_font)
    plt.ylabel('单位净值', fontproperties=my_font)
    plt.title(f"{foundCode} 基金走势", fontproperties=my_font)
    plt.xticks(x[::90], found_price_x[::90], rotation=45)

    plt.show()


# show_found(found_price_y)

def calculate_found_profit():
    start_date = datetime.datetime.fromisoformat('2015-06-10')
    end_date = datetime.datetime.fromisoformat('2020-03-01')
    result = calculate_found_profit_by_month(start_date, end_date)
    print(result)

# calculate_found_profit()
