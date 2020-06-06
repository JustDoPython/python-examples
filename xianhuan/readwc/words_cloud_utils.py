#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
from os import path
import numpy as np
import jieba.analyse
from PIL import Image
from wordcloud import WordCloud
from matplotlib import pyplot as plt


class WordsCloudUtils:

    default_path = path.dirname(__file__)
    default_pic_name = 'wc.png' # 默认输出图片名称
    default_stop_words_file = 'stopwordsbd.txt' # 停用词库
    default_font_path = '/System/Library/Fonts/PingFang.ttc' # 字体库路径，下载字体后，替换成自己电脑的存放路径，这里是Mac的存放路径

    # 分词
    @staticmethod
    def split_text(text):
        all_seg = jieba.cut(text, cut_all=False)
        all_word = ' '
        for seg in all_seg:
            all_word = all_word + seg + ' '

        return all_word

    @staticmethod
    def gen_wc_split_text(text='There is no txt', max_words=None, background_color=None,
                          font_path=default_font_path,
                          output_path=default_path, output_name=default_pic_name,
                          mask_path=None, mask_name=None,
                          width=400, height=200, max_font_size=100, axis='off'):
        split_text = WordsCloudUtils.split_text(text)

        # 设置一个底图
        mask = None
        if mask_path is not None:
            mask = np.array(Image.open(path.join(mask_path, mask_name)))

        wordcloud = WordCloud(background_color=background_color,
                              mask=mask,
                              max_words=max_words,
                              max_font_size=max_font_size,
                              width=width,
                              height=height,
                              # 如果不设置中文字体，可能会出现乱码
                              font_path=font_path)
        myword = wordcloud.generate(str(split_text))
        # 展示词云图
        plt.imshow(myword)
        plt.axis(axis)
        plt.show()

        # 保存词云图
        wordcloud.to_file(path.join(output_path, output_name))

    @staticmethod
    def gen_wc_file(file_path, max_words=None, background_color=None,
                    font_path=default_font_path,
                    output_path=default_path, output_name=default_pic_name,
                    mask_path=None, mask_name=None,
                    width=400, height=200, max_font_size=100, axis='off'):
        if not len(file_path):
            print('没有文件路径！')
            raise Exception('没有文件路径！')

        with open(file_path) as file:
            jieba.analyse.set_stop_words(path.join(WordsCloudUtils.default_path, WordsCloudUtils.default_stop_words_file))  # 设置止词列表
            tags = jieba.analyse.extract_tags(file.read(), 1000, withWeight=True)
            data = {item[0]: item[1] for item in tags}
            # 设置一个底图
            mask = None
            if mask_path is not None:
                mask = np.array(Image.open(path.join(mask_path, mask_name)))
            wordcloud = WordCloud(background_color=background_color,
                                  mask=mask,
                                  max_words=max_words,
                                  max_font_size=max_font_size,
                                  width=width,
                                  height=height,
                                  # 如果不设置中文字体，可能会出现乱码
                                  font_path=font_path).generate_from_frequencies(data)

            # 展示词云图
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis(axis)
            plt.show()

            # 保存词云图
            wordcloud.to_file(path.join(output_path, output_name))

    @staticmethod
    def gen_wc_tags(tags, max_words=None, background_color=None,
                    font_path=default_font_path,
                    output_path=default_path, output_name=default_pic_name,
                    mask_path=None, mask_name=None,
                    width=400, height=200, max_font_size=100, axis='off'):
        # 设置一个底图
        mask = None
        if mask_path is not None:
            mask = np.array(Image.open(path.join(mask_path, mask_name)))
        wordcloud = WordCloud(background_color=background_color,
                              mask=mask,
                              max_words=max_words,
                              max_font_size=max_font_size,
                              width=width,
                              height=height,
                              # 如果不设置中文字体，可能会出现乱码
                              font_path=font_path).generate_from_frequencies(tags)

        # 展示词云图
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis(axis)
        plt.show()

        # 保存词云图
        wordcloud.to_file(path.join(output_path, output_name))


if __name__ == '__main__':
    # 传入3个参数：文章文件路径，底图路径，地图图片名称
    WordsCloudUtils.gen_wc_file('./gzbg2020', mask_path='./', mask_name='blackheart.jpeg')