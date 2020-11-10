import requests
import time
import pandas as pd
from lxml import etree
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Line
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud

base_url = 'https://movie.douban.com/subject/35155748/comments?start={}&limit=20&status=P&sort={}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'Referer': 'https://movie.douban.com',
    # 注意，这里需要加上你自己的 cookie
    'Cookie': '.'
}


def get_comments():
    user_list, star_list, time_list, comment_list = [], [], [], []
    for sort in ['time', 'new_score']:
        sort_name = "最热" if sort == 'new_score' else '最新'
        for start in range(25):
            print('准备抓取第 {} 页数据, 排序方式：{}'.format(start + 1, sort_name))
            users, stars, times, comments = get_comment_by_url(base_url.format(start * 20, sort))
            if not users:
                break
            user_list += users
            star_list += stars
            time_list += times
            comment_list += comments
            # 每次获取数据之后暂停 5 秒
            time.sleep(5)
            print("#" * 10)
            print(user_list)
            print(star_list)
            print(time_list)
            print(comment_list)
            print("#" * 10)

    comments_dic = {'users': user_list, 'times': time_list, 'stars': star_list, 'comments': comment_list}
    return comments_dic


def get_comment_by_url(url):
    # 用户、评论等级、评论时间、评论内容
    users, stars, times, content_list = [], [], [], []
    data = requests.get(url, headers=headers)
    selector = etree.HTML(data.text)
    comments = selector.xpath('//div[@class="comment"]')
    # 遍历所有评论
    for comment in comments:
        user = comment.xpath('.//h3/span[2]/a/text()')[0]
        star = comment.xpath('.//h3/span[2]/span[2]/@class')[0][7:8]
        date_time = comment.xpath('.//h3/span[2]/span[3]/text()')
        if len(date_time) != 0:
            date_time = date_time[0].replace("\n", "").strip()
        else:
            date_time = None
        comment_text = comment.xpath('.//p/span/text()')[0].strip()
        users.append(user)
        stars.append(star)
        times.append(date_time)
        content_list.append(comment_text)
    return users, stars, times, content_list


def format_data(result, key):
    list_ = []
    for value in result[key].values():
        list_.append(value)
    return list_


# 数量
def show_num(df):
    df_time = df.groupby(['times']).size()
    values = df_time.values.tolist()
    index = df_time.index.tolist()
    bar = Bar()
    bar.add_xaxis(index)
    bar.add_yaxis("数量 & 时间", values)
    bar.set_global_opts(xaxis_opts=opts.AxisOpts(name="评论日期", axislabel_opts={"rotate": 30}))
    bar.render_notebook()


# 星级
def show_star(df):
    df_time = df.groupby(['times']).size()
    dic = {}

    for k in df_time.index:
        stars = df.loc[df['times'] == str(k), 'stars']
        stars = list(map(int, stars))
        dic[k] = round(sum(stars) / len(stars), 2)

    bar_star = Bar()
    bar_star.add_xaxis([x for x in dic.keys()])
    bar_star.add_yaxis("星级 & 时间", [x for x in dic.values()])
    bar_star.set_global_opts(xaxis_opts=opts.AxisOpts(name="评论日期", axislabel_opts={"rotate": 30}))
    bar_star.render_notebook()


# 演员
def show_actor(df):
    roles = {'张译': 0, '吴京': 0, '李九霄': 0, '魏晨': 0, '邓超': 0}
    names = list(roles.keys())

    for row in df['comments']:
        for name in names:
            roles[name] += row.count(name)

    line = (
        Line()
            .add_xaxis(list(roles.keys()))
            .add_yaxis('', list(roles.values()))
            .set_global_opts(title_opts=opts.TitleOpts(title=""))
    )

    line.render_notebook()


# 词云
def show_word_cloud(df):
    content = "".join(list(df['comments']))

    # 分词
    words = jieba.cut(content)
    word_list = []
    for x in words:
        word_list.append(x)
    cloud_word = ','.join(word_list)
    wc = WordCloud(font_path='/System/Library/Fonts/PingFang.ttc', background_color="white", scale=2.5,
                   contour_color="lightblue", ).generate(cloud_word)

    plt.figure(figsize=(16, 9))
    plt.imshow(wc)
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    result = get_comments()
    users = format_data(result, 'users')
    stars = format_data(result, 'stars')
    times = format_data(result, 'times')
    comments = format_data(result, 'comments')

    comments_dic = {'users': users, 'times': times, 'stars': stars, 'comments': comments}
    df = pd.DataFrame(comments_dic)
    df = df.drop_duplicates()

    # show_num(df)
    # show_star(df)
    # show_actor(df)
    # show_word_cloud(df)
