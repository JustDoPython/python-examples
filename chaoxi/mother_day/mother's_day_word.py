import numpy
import multidict
import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator

def transform_format(val):
    """
    用于去除杂色
    Arguments:
        val {[array]} -- RGB颜色组
    Returns:
        [array] -- 去除杂色后的值
    """
    if val[0] > 245 and val[1] > 245 and val[2] > 245:
        val[0] = val[1] = val[2] = 255
        return val
    else:
        return val


def gen_happy_birthday_cloud(file, name):
    words = multidict.MultiDict()
    # 必须先初始化两个最大权重的
    words.add('母亲节快乐', 12)
    words.add(name, 10)

    # 随意插入新的词语
    for i in range(1000):
        words.add('亲爱的妈妈', numpy.random.randint(1, 5))
        words.add('您辛苦了', numpy.random.randint(1, 5))
        words.add(name, numpy.random.randint(1, 5))

    # 设定图片
    bimg = imread(file)
    for color in range(len(bimg)):
        bimg[color] = list(map(transform_format, bimg[color]))

    wordcloud = WordCloud(
        background_color='pink',
        mask=bimg,
        font_path='simhei.ttf'
    ).generate_from_frequencies(words)

    # 生成词云
    bimgColors = ImageColorGenerator(bimg)

    # 渲染词云
    plt.axis("off")
    plt.imshow(wordcloud.recolor(color_func=bimgColors))
    plt.savefig(name + '.png')
    plt.show()

gen_happy_birthday_cloud("mother1.jpg", "母亲节")
