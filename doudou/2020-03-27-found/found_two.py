import json
import datetime
import calendar
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts import options as opts

foundCode = '510300'
fixed_investment_amount_per_week = 500 # 每周定投金额
fixed_investment_amount_per_month = 2000 # 每月定投金额

def get_data():
    with open(f'./found_{foundCode}.txt') as f:
        line = f.readline()
        result = json.loads(line)
        found_date_price = {}
        for found in result['Data']['LSJZList'][::-1]:
            found_date_price[found['FSRQ']] = found['DWJZ']
        return found_date_price

found_date_price = get_data()

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
    # 周定投收益
    for i in range(5):
        result = calculate_found_profit_by_week(start_date, end_date, i)
        total_amount.append(result[2])
        total_profit.append(result[3])
    # 月定投收益
    result_month = calculate_found_profit_by_month(start_date, end_date)
    total_amount.append(result_month[2])
    total_profit.append(result_month[3])
    return total_amount, total_profit

total_amount, total_profit = calculate_found_profit_week_month()

# 这部分代码在 jupyter 中 run
line = (
    Line()
    .add_xaxis(list(found_date_price.keys()))
    .add_yaxis('price',list(found_date_price.values()),label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title=f'{foundCode}基金走势图'),
        xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
        yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
    )
)
#line.render_notebook()

x = ['周一', '周二', '周三', '周四', '周五', '月定投']
bar = (
    Bar()
    .add_xaxis(x)
    .add_yaxis('投资金额', total_amount)
    .add_yaxis('投资收益', total_profit)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="投资总额 & 投资收益"),
        xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
        yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
    )
)
#bar.render_notebook()
# 这部分代码在 jupyter 中 run

start_date = datetime.datetime.fromisoformat('2015-06-10')
end_date = datetime.datetime.fromisoformat('2020-03-01')
result = calculate_found_profit_by_month(start_date, end_date)
print(result)