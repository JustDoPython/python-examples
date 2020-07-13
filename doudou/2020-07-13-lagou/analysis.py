import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json
import pandas as pd


def get_data():
    with open('data.txt') as f:
        data = []
        for line in f.readlines():
            result = json.loads(line)
            result_list = result['content']['positionResult']['result']
            for item in result_list:
                dict = {
                    'city': item['city'],
                    'industryField': item['industryField'],
                    'education': item['education'],
                    'workYear': item['workYear'],
                    'salary': item['salary'],
                    'firstType': item['firstType'],
                    'secondType': item['secondType'],
                    'thirdType': item['thirdType'],
                    # list
                    'skillLables': ','.join(item['skillLables']),
                    'companyLabelList': ','.join(item['companyLabelList'])
                }
                data.append(dict)
        return data


data = get_data()
data = pd.DataFrame(data)
data.head(5)

# 城市图
citys_value_counts = data['city'].value_counts()
top = 15
citys = list(citys_value_counts.head(top).index)
city_counts = list(citys_value_counts.head(top))

bar = (
    Bar()
        .add_xaxis(citys)
        .add_yaxis("", city_counts)
)
bar.render_notebook()

# 城市图
pie = (
    Pie()
        .add("", [list(z) for z in zip(citys, city_counts)])
        .set_global_opts(title_opts=opts.TitleOpts(title=""))
        .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
)
pie.render_notebook()

# 行业
industrys = list(data['industryField'])
industry_list = [i for item in industrys for i in item.split(',')]

industry_series = pd.Series(data=industry_list)
industry_value_counts = industry_series.value_counts()

industrys = list(industry_value_counts.head(top).index)
industry_counts = list(industry_value_counts.head(top))

pie = (
    Pie()
        .add("", [list(z) for z in zip(industrys, industry_counts)])
        .set_global_opts(title_opts=opts.TitleOpts(title=""))
        .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
)
pie.render_notebook()

# 学历
eduction_value_counts = data['education'].value_counts()

eduction = list(eduction_value_counts.index)
eduction_counts = list(eduction_value_counts)

pie = (
    Pie()
        .add("", [list(z) for z in zip(eduction, eduction_counts)])
        .set_global_opts(title_opts=opts.TitleOpts(title=""))
        .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
)
pie.render_notebook()

# 工作年限
work_year_value_counts = data['workYear'].value_counts()
work_year = list(work_year_value_counts.index)
work_year_counts = list(work_year_value_counts)

bar = (
    Bar()
        .add_xaxis(work_year)
        .add_yaxis("", work_year_counts)
)
bar.render_notebook()

# 技能
word_data = data['skillLables'].str.split(',').apply(pd.Series)
word_data = word_data.replace(np.nan, '')
text = word_data.to_string(header=False, index=False)

wc = WordCloud(font_path='/System/Library/Fonts/PingFang.ttc', background_color="white", scale=2.5,
               contour_color="lightblue", ).generate(text)

plt.figure(figsize=(16, 9))
plt.imshow(wc)
plt.axis('off')
plt.show()

# 福利
word_data = data['companyLabelList'].str.split(',').apply(pd.Series)
word_data = word_data.replace(np.nan, '')
text = word_data.to_string(header=False, index=False)

wc = WordCloud(font_path='/System/Library/Fonts/PingFang.ttc', background_color="white", scale=2.5,
               contour_color="lightblue", ).generate(text)

plt.figure(figsize=(16, 9))
plt.imshow(wc)
plt.axis('off')
plt.show()

# 薪资
salary_value_counts = data['salary'].value_counts()
salary = list(salary_value_counts.head(top).index)
salary_counts = list(salary_value_counts.head(top))

bar = (
    Bar()
        .add_xaxis(salary)
        .add_yaxis("", salary_counts)
        .set_global_opts(xaxis_opts=opts.AxisOpts(name_rotate=0, name="薪资", axislabel_opts={"rotate": 45}))
)
bar.render_notebook()
