from wordcloud import WordCloud
import numpy as np, jieba
from PIL import Image

def jieba_():
    stop_words = []
    with open('stop_words.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            stop_words.append(line.strip())
    content = open('aljx.txt', 'rb').read()
    # jieba 分词
    word_list = jieba.cut(content)
    words = []
    for word in word_list:
        if word not in stop_words:
            words.append(word)
    global word_cloud
    # 用逗号隔开词语
    word_cloud = '，'.join(words)

def cloud():
    # 打开词云背景图
    cloud_mask = np.array(Image.open('bg.png'))
    # 定义词云的一些属性
    wc = WordCloud(
        # 背景图分割颜色为白色
        background_color='white',
        # 背景图样
        mask=cloud_mask,
        # 显示最大词数
        max_words=300,
        # 显示中文
        font_path='./fonts/simhei.ttf',
        # 最大尺寸
        max_font_size=100
    )
    global word_cloud
    # 词云函数
    x = wc.generate(word_cloud)
    # 生成词云图片
    image = x.to_image()
    # 展示词云图片
    image.show()
    # 保存词云图片
    wc.to_file('cloud.png')

jieba_()
cloud()