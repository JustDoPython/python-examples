import json
import jieba
from PIL import Image
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import numpy as np
from os import path


month_data = {}
with open(r"c:\pworkspace\mypy\pythontech\weibohot\comments.txt", "r", encoding="utf-8") as f:
    for line in f:
        data_obj = json.loads(line)
        date = data_obj['date']
        month_str = date[3:5]
        data_list = []
        if month_str in month_data:
            data_list =  month_data[month_str]
        data_list.append(data_obj)
        month_data[month_str] = data_list


def gen_wc_split_text(data_list=[], max_words=None, background_color=None,
                      # font_path='/System/Library/Fonts/PingFang.ttc',
                      font_path=r'C:\Windows\Fonts\simhei.ttf',
                      output_path='', output_name='',
                      mask_path=None, mask_name=None,
                      width=400, height=200, max_font_size=100, axis='off'):
    stopwords = open(r'c:\pworkspace\mypy\pythontech\weibohot\stopwords.txt', 'r', encoding='utf-8').read().split('\n')[:-1]
    words_dict = {}
    for data in data_list:
        text = data['topic']
        hotNumber = data['hotNumber']
        if hotNumber is None:
            hotNumber = 1
        all_seg = jieba.cut(text, cut_all=False)
        for seg in all_seg:
            if seg in stopwords or seg == 'unknow':
                continue
            if seg in words_dict.keys():
                words_dict[seg] += hotNumber
            else:
                words_dict[seg] = hotNumber

    # 设置一个底图
    mask = None
    if mask_path is not None:
        mask = np.array(Image.open(path.join(mask_path, mask_name)))

    wordcloud = WordCloud(background_color=background_color,
                          mask=mask,
                          max_words=max_words,
                          min_font_size=1,
                          max_font_size=50,
                          width=300,
                          height=400,
                          # 如果不设置中文字体，可能会出现乱码
                          font_path=font_path)
    myword = wordcloud.generate_from_frequencies(words_dict)
    # 展示词云图
    # plt.imshow(myword)
    # plt.axis(axis)
    # plt.show()

    # 保存词云图
    wordcloud.to_file(path.join(output_path, output_name))


for month in month_data:
    data_list = month_data[month]
    
    gen_wc_split_text(data_list, output_name=month+'.png',background_color='white',  
    mask_path=r"c:\pworkspace\mypy\pythontech\weibohot", mask_name="0"+month+".jpg", max_words=2000, 
    output_path=r"c:\pworkspace\mypy\pythontech\weibohot")


