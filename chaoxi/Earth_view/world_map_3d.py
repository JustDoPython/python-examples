import pyecharts.options as opts
from pyecharts.charts import MapGlobe
from pyecharts.faker import POPULATION


data = [x for _, x in POPULATION[1:]]
low, high = min(data), max(data)
c = (
    MapGlobe(init_opts=opts.InitOpts(width='1000px', height='1000px',bg_color='#00BBFF'))#
    .add_schema()
    .add(
        maptype="world",
        series_name="World Population",
        data_pair=POPULATION[1:],
        is_map_symbol_show=True,
        label_opts=opts.LabelOpts(is_show=True),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="3D 地球示例"),
        # 设置地球属性
        visualmap_opts=opts.VisualMapOpts(
            min_=low,
            max_=high,
            range_text=["max", "min"],
            is_calculable=True,
            range_color=["lightskyblue", "yellow", "orangered"],
        )
    )
    .render("world_map_3d.html")
)