#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
import io
from PIL import Image
import requests


def get_word(ch, quality):
    """获取单个汉字（字符）的图片
    ch          - 单个汉字或英文字母（仅支持大写）
    quality     - 单字分辨率，H-640像素，M-480像素，L-320像素
    """

    fp = io.BytesIO(requests.post(url='http://xufive.sdysit.com/tk', data={'ch': ch}).content)
    im = Image.open(fp)
    w, h = im.size
    if quality == 'M':
        w, h = int(w * 0.75), int(0.75 * h)
    elif quality == 'L':
        w, h = int(w * 0.5), int(0.5 * h)

    return im.resize((w, h))


def get_bg(quality):
    """获取春联背景的图片"""

    return get_word('bg', quality)


def write_couplets(text, HorV='V', quality='L', out_file=None):
    """生成春联

    text        - 春联内容，以空格断行
    HorV        - H-横排，V-竖排
    quality     - 单字分辨率，H-640像素，M-480像素，L-320像素
    out_file    - 输出文件名
    """

    usize = {'H': (640, 23), 'M': (480, 18), 'L': (320, 12)}
    bg_im = get_bg(quality)
    text_list = [list(item) for item in text.split()]
    rows = len(text_list)
    cols = max([len(item) for item in text_list])

    if HorV == 'V':
        ow, oh = 40 + rows * usize[quality][0] + (rows - 1) * 10, 40 + cols * usize[quality][0]
    else:
        ow, oh = 40 + cols * usize[quality][0], 40 + rows * usize[quality][0] + (rows - 1) * 10
    out_im = Image.new('RGBA', (ow, oh), '#f0f0f0')

    for row in range(rows):
        if HorV == 'V':
            row_im = Image.new('RGBA', (usize[quality][0], cols * usize[quality][0]), 'white')
            offset = (ow - (usize[quality][0] + 10) * (row + 1) - 10, 20)
        else:
            row_im = Image.new('RGBA', (cols * usize[quality][0], usize[quality][0]), 'white')
            offset = (20, 20 + (usize[quality][0] + 10) * row)

        for col, ch in enumerate(text_list[row]):
            if HorV == 'V':
                pos = (0, col * usize[quality][0])
            else:
                pos = (col * usize[quality][0], 0)

            ch_im = get_word(ch, quality)
            row_im.paste(bg_im, pos)
            row_im.paste(ch_im, (pos[0] + usize[quality][1], pos[1] + usize[quality][1]), mask=ch_im)

        out_im.paste(row_im, offset)

    if out_file:
        out_im.convert('RGB').save(out_file)
    out_im.show()


# text = '龙引千江水 虎越万重山'
# write_couplets(text, HorV='V', quality='M', out_file='竖联.jpg')

text = '龙腾虎跃'
write_couplets(text, HorV='H', quality='M', out_file='横联.jpg')