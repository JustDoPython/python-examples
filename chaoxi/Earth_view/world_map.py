from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker

c = (
    Map(init_opts=opts.InitOpts(width='1500px', height='1200px',bg_color='#E0EEEE'))
    # 加载世界地图实例
    .add("世界地图", [list(z) for z in zip(Faker.country, Faker.values())], "world")
   # 不显示地图标志
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        # 配置项标题设置
        title_opts=opts.TitleOpts(title="世界地图示例"),
        visualmap_opts=opts.VisualMapOpts(max_=200)
    )
    # 生成超文本文件
    .render("world_map.html")
)




