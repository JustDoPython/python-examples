from pyecharts import options as opts
from pyecharts.charts import Map3D
from pyecharts.globals import ChartType

# 写入省份内各地区经纬度
example_data = [
    [[106.70722,26.59820, 1000],[106.63024, 26.64702, 1000]],
    [[104.83023, 26.59336], [106.92723, 27.72545]],
    [[105.30504, 27.29847], [107.52034, 26.29322]],
    [[107.89868, 26.52881], [104.948571, 25.077502]],
    [[105.9462, 26.25367], [109.18099, 27.69066]],
]
#　添加 3D 地图
c = (
    Map3D(init_opts=opts.InitOpts(width='1200px', height='1200px'))
    .add_schema(
        maptype="贵州",
        itemstyle_opts=opts.ItemStyleOpts(
            color="rgb(5,101,123)",
            opacity=1,
            border_width=0.8,
            border_color="rgb(62,215,213)",
        ),
        light_opts=opts.Map3DLightOpts(
            main_color="#fff",
            main_intensity=1.2,
            is_main_shadow=True,
            main_alpha=55,
            main_beta=10,
            ambient_intensity=0.3,
        ),
        view_control_opts=opts.Map3DViewControlOpts(center=[-10, 0, 10]),
        post_effect_opts=opts.Map3DPostEffectOpts(is_enable=True),

    )
    .add(
        series_name="",
        data_pair=example_data,
        type_=ChartType.LINES3D,
        effect=opts.Lines3DEffectOpts(
            is_show=True,
            period=4,
            trail_width=3,
            trail_length=0.5,
            trail_color="#f00",
            trail_opacity=1,
        ),
        label_opts=opts.LabelOpts(is_show=True),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="Map3D-GuiZhou3D"))
    .render("guizhou_map_3d.html")
)
