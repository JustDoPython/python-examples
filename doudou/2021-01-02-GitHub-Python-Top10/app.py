import requests
from pyecharts.charts import Bar
from pyecharts import options as opts


def get_data():
    base_url = 'https://api.github.com/search/repositories?q=language:python+created:%3E2019-12-31&sort=stars&order=desc&per_page=10'
    response = requests.get(base_url)
    result = response.json()
    data = {}
    for item in result['items']:
        data[item['name']] = [item['html_url'], item['stargazers_count'], item['watchers_count'], item['forks']]
    return data


def show_img():
    data = get_data()
    names = list(data.keys())
    values = [data[name][1] for name in names]

    bar = (
        Bar()
            .add_xaxis(names[::-1])
            .add_yaxis("星标数", values[::-1])
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(name_rotate=0, name="项目", axislabel_opts={'interval': -10, "rotate": 0}),
            title_opts=opts.TitleOpts(title="2020 GitHub Python TOP 10"))
    )
    bar.render_notebook()


if __name__ == '__main__':
    show_img()
