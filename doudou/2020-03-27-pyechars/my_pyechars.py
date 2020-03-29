from pyecharts.charts import Bar
from pyecharts.charts import Pie
from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.charts import EffectScatter
from pyecharts.globals import SymbolType
from pyecharts.charts import Grid
from pyecharts.charts import WordCloud
from pyecharts.charts import Map
import random


x = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
data_china = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
data_russia = [1.6, 5.4, 9.3, 28.4, 22.7, 60.7, 162.6, 199.2, 56.7, 43.8, 3.0, 4.9]


# 柱状图
bar = Bar()
bar.add_xaxis(x)
bar.add_yaxis("降水量", data_china)
bar.set_global_opts(title_opts=opts.TitleOpts(title="Bar - 基本示例"))
bar.render()


bar = (
    Bar()
    .add_xaxis(x)
    .add_yaxis('china', data_china)
    .set_global_opts(title_opts=opts.TitleOpts(title="Bar - 基本示例"))
)
bar.render_notebook()


bar = (
    Bar()
    .add_xaxis(x)
    .add_yaxis('china', data_china)
    .add_yaxis("sussia", data_russia)
    .set_global_opts(title_opts=opts.TitleOpts(title="Bar - 多柱状图"))
)
bar.render_notebook()


bar = (
    Bar()
    .add_xaxis(x)
    .add_yaxis('china', data_china)
    .add_yaxis('russia', data_russia)
    .reversal_axis()
    .set_series_opts(label_opts=opts.LabelOpts(position="right"))
    .set_global_opts(title_opts=opts.TitleOpts(title="Bar - 翻转 XY 轴"))
)
bar.render_notebook()

# 饼状图
pie = (
    Pie()
    .add("", [list(z) for z in zip(x, data_china)])
    .set_global_opts(title_opts=opts.TitleOpts(title="Pie - 基本示例"))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
)
pie.render_notebook()


pie = (
    Pie(init_opts=opts.InitOpts(width="600px", height="400px"))
    .add(
        series_name="降雨量",
        data_pair=[list(z) for z in zip(x, data_china)],
        radius=["50%", "70%"],
        label_opts=opts.LabelOpts(is_show=False, position="center"),
    )
    .set_global_opts(legend_opts=opts.LegendOpts(pos_left="legft", orient="vertical"))
    .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),
    label_opts=opts.LabelOpts(formatter="{b}: {c}")
    )
)
pie.render_notebook()


# 折线图
line = (
    Line()
    .add_xaxis(x)
    .add_yaxis('china', data_china)
    .set_global_opts(title_opts=opts.TitleOpts(title="Line - 基本示例"))
)
line.render_notebook()


line = (
    Line()
    .add_xaxis(x)
    .add_yaxis('china', data_china)
    .add_yaxis('russis', data_russia)
    .set_global_opts(title_opts=opts.TitleOpts(title="Line - 双折线图"))
)
line.render_notebook()


line = (
    Line()
    .add_xaxis(x)
    .add_yaxis('china', data_china, is_step=True)
    .set_global_opts(title_opts=opts.TitleOpts(title="Line - 阶梯折线图"))
)
line.render_notebook()


# 散点图
scatter = (
    EffectScatter()
    .add_xaxis(x)
    .add_yaxis("", data_china)
    .set_global_opts(title_opts=opts.TitleOpts(title="EffectScatter - 基本示例"))
)
scatter.render_notebook()


scatter = (
    EffectScatter()
    .add_xaxis(x)
    .add_yaxis("china", data_china, symbol=SymbolType.ARROW)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="EffectScatter - 显示分割线"),
        xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
        yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
    )
)
scatter.render_notebook()


scatter = (
    EffectScatter()
    .add_xaxis(x)
    .add_yaxis("china", [x + 30 for x in data_russia],symbol=SymbolType.ARROW)
    .add_yaxis("russia", data_russia, symbol=SymbolType.TRIANGLE)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="EffectScatter - 显示分割线"),
        xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
        yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
    )
)
scatter.render_notebook()


# 图表合并
bar = (
    Bar()
    .add_xaxis(x)
    .add_yaxis('china', data_china)
    .add_yaxis("sussia", data_russia)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Grid - 多图合并"),
    )
)

line = (
    Line()
    .add_xaxis(x)
    .add_yaxis("蒸发量", [x + 50 for x in data_china]
    )
)

bar.overlap(line)
grid = Grid()
grid.add(bar, opts.GridOpts(pos_left="5%", pos_right="5%"), is_control_axis_index=True)
grid.render_notebook()


# 词云
data = [("生活资源", "999"),("供热管理", "888"),("供气质量", "777"),("生活用水管理", "688"),("一次供水问题", "588"),("交通运输", "516"),("城市交通", "515"),("环境保护", "483"),("房地产管理", "462"),("城乡建设", "449"),("社会保障与福利", "429"),("社会保障", "407"),("文体与教育管理", "406"),("公共安全", "406"),("公交运输管理", "386"),("出租车运营管理", "385"),("供热管理", "375"),("市容环卫", "355"),("自然资源管理", "355"),("粉尘污染", "335"),("噪声污染", "324"),("土地资源管理", "304"),("物业服务与管理", "304"),("医疗卫生", "284"),("粉煤灰污染", "284"),("占道", "284"),("供热发展", "254"),("农村土地规划管理", "254"),("生活噪音", "253"),("供热单位影响", "253"),("城市供电", "223"),("房屋质量与安全", "223"),("大气污染", "223"),("房屋安全", "223"),("文化活动", "223"),("拆迁管理", "223"),("公共设施", "223"),("供气质量", "223"),("供电管理", "223"),("燃气管理", "152"),("教育管理", "152"),("医疗纠纷", "152"),("执法监督", "152"),("设备安全", "152"),("政务建设", "152"),("县区、开发区", "152"),("宏观经济", "152"),("教育管理", "112"),("社会保障", "112"),("生活用水管理", "112"),("物业服务与管理", "112"),("分类列表", "112"),("农业生产", "112"),("二次供水问题", "112"),("城市公共设施", "92"),("拆迁政策咨询", "92"),("物业服务", "92"),("物业管理", "92"),("社会保障保险管理", "92"),("低保管理", "92"),("文娱市场管理", "72"),("城市交通秩序管理", "72"),("执法争议", "72"),("商业烟尘污染", "72"),("占道堆放", "71"),("地上设施", "71"),("水质", "71"),("无水", "71"),("供热单位影响", "71"),("人行道管理", "71"),("主网原因", "71"),("集中供热", "71"),("客运管理", "71"),("国有公交（大巴）管理", "71"),("工业粉尘污染", "71"),("治安案件", "71"),("压力容器安全", "71"),("身份证管理", "71"),("群众健身", "41"),("工业排放污染", "41"),("破坏森林资源", "41"),("市场收费", "41"),("生产资金", "41"),("生产噪声", "41"),("农村低保", "41"),("劳动争议", "41"),("劳动合同争议", "41"),("劳动报酬与福利", "41"),("医疗事故", "21"),("停供", "21"),("基础教育", "21"),("职业教育", "21"),("物业资质管理", "21"),("拆迁补偿", "21"),("设施维护", "21"),("市场外溢", "11"),("占道经营", "11"),("树木管理", "11"),("农村基础设施", "11"),("无水", "11"),("供气质量", "11"),("停气", "11"),("市政府工作部门（含部门管理机构、直属单位）", "11"),("燃气管理", "11"),("市容环卫", "11"),("新闻传媒", "11"),("人才招聘", "11"),("市场环境", "11"),("行政事业收费", "11"),("食品安全与卫生", "11"),("城市交通", "11"),("房地产开发", "11"),("房屋配套问题", "11"),("物业服务", "11"),("物业管理", "11"),("占道", "11"),("园林绿化", "11"),("户籍管理及身份证", "11"),("公交运输管理", "11"),("公路（水路）交通", "11"),("房屋与图纸不符", "11"),("有线电视", "11"),("社会治安", "11"),("林业资源", "11"),("其他行政事业收费", "11"),("经营性收费", "11"),("食品安全与卫生", "11"),("体育活动", "11"),("有线电视安装及调试维护", "11"),("低保管理", "11"),("劳动争议", "11"),("社会福利及事务", "11"),("一次供水问题", "11"),]

wordCloud = (
    WordCloud()
    .add(series_name="热点分析", data_pair=data, word_size_range=[6, 66])
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="热点分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True),
    )
)

wordCloud.render_notebook()


# 地图
provinces = ['广东', '北京', '上海', '湖南', '重庆', '新疆', '河南', '黑龙江', '浙江', '台湾']
values = [random.randint(1, 1024) for x in range(len(provinces))]

map = (
    Map()
    .add("", [list(z) for z in zip(provinces, values)], "china")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="map - 基本示例"),
        visualmap_opts=opts.VisualMapOpts(max_=1024, is_piecewise=True),
    )

)
map.render_notebook()