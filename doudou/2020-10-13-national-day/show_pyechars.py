import csv
import pandas as pd
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import ChartType, SymbolType
from pyecharts.charts import Bar
from pyecharts.charts import Pie

data = []
with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        data.append(row)

df_data = []
for row in data:
    city = row[1].split('·')[1]
    if city in ['保亭', '德宏', '湘西', '陵水', '黔东南', '黔南']:
        continue
    star = row[4].split('热度')[1].strip()
    star = int(float(star) * 1000)
    df_data.append([row[0], city, row[3], star])

df = pd.DataFrame(df_data, columns=['name', 'city', 'level', 'star'])


def show_pic_one():
    data = df.groupby(by=['city'])['star'].sum()
    citys = list(data.index)
    city_stars = list(data)

    data = [list(z) for z in zip(citys, city_stars)]
    geo = (
        Geo()
            .add_schema(maptype="china")
            .add(
            "热点图",  # 图题
            data,
            type_=ChartType.HEATMAP,  # 地图类型
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 设置是否显示标签
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=5000),  # 设置legend显示的最大值
            title_opts=opts.TitleOpts(title=""),  # 左上角标题
        )
    )

    geo.render_notebook()


def show_pic_two():
    data = df.loc[:, 'city'].value_counts().sort_values(ascending=False)
    citys = list(data.index)[:15]
    city_count = list(data)[:15]

    bar = Bar()
    bar.add_xaxis(citys)
    bar.add_yaxis("Top 15", city_count)
    bar.set_global_opts(title_opts=opts.TitleOpts(title=""))
    bar.render_notebook()


def show_pic_three():
    data = df.groupby(by=['name'])['star'].sum().sort_values(ascending=False)
    names = list(data.index)[:10]
    name_stars = list(data)[:10]

    # data

    pie = (
        Pie()
            .add("", [list(z) for z in zip(names, name_stars)])
            .set_global_opts(title_opts=opts.TitleOpts(title=""))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    pie.render_notebook()
