#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
from tkinter import Tk, Label, Entry, ttk, Button, StringVar
from urllib.request import urlretrieve

import requests
import re
from PIL import Image, ImageTk


class artName:
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    def get_sign(self):
        name = self.name_entry.get()
        font = self.combox_list.get()
        mapping_list = {
            "行书签": "6.ttf",
            "超级艺术签": "7.ttf",
            "潇洒签": "8.ttf",
            "手写连笔字": "9.ttf",
            "行草签": "11.ttf",
            "花式签": "12.ttf",
            "温柔女生": "13.ttf",
            "个性签": "15.ttf",
            "商务签": "16.ttf",
            "正楷体": "17.ttf",
            "楷书签": "19.ttf",
            "情书签": "20.ttf",
            "卡通可爱签": "25.ttf"
        }
        url = 'http://www.kachayv.cn/'
        data = {
            'word': name,
            'fonts': mapping_list[font],
            'sizes': 60,
            'fontcolor': '#ffffff',
            'colors': '#FD5668'
        }
        result = requests.post(url, data=data)
        result.encoding = 'utf-8'
        html = result.text
        print(html)
        p = re.compile('<img id="showImg" src="cache/(.*?)"/>')
        match = p.findall(html)
        urlretrieve('http://www.kachayv.cn/cache/' + match[0], './pic.jpg')
        img = Image.open('./pic.jpg')
        photo = ImageTk.PhotoImage(img, master=self.init_window)
        self.pic_label.config(image=photo)
        self.pic_label.image=photo


    def draw_window(self):
        self.init_window = Tk()
        self.init_window.title("阿花专属签名设计")
        self.init_window.geometry("800x500")
        self.init_window.geometry("+400+200")

        # 姓名
        self.name_label = Label(self.init_window, text='鼎鼎大名', font=('微软雅黑', 16), fg='black')
        self.name_label.grid(row=0, column=0, columnspan=1)
        self.name_entry = Entry(self.init_window, font=('宋体', 16))
        self.name_entry.grid(row=0, column=1)

        # 选择字体模式
        self.font_label = Label(self.init_window, text='字体', font=('微软雅黑', 16), fg='black')
        self.font_label.grid(row=0, column=5, columnspan=1)
        self.combox_list = ttk.Combobox(self.init_window, textvariable=StringVar())
        self.combox_list.grid(row=0, column=6, sticky='W')
        self.combox_list["value"] = ("行书签", "超级艺术签", "潇洒签", "手写连笔字", "行草签", "花式签", "温柔女生", "个性签",
                                     "商务签", "正楷体", "楷书签", "情书签", "卡通可爱签")
        self.combox_list.current(0)  # 选择第一个

        # 触发按钮
        self.button = Button(self.init_window, text='美好来袭', font=('微软雅黑', 16), command=self.get_sign)
        self.button.grid(row=1, column=3, rowspan=2, sticky='W')

        # 图片展示
        self.pic_label = Label(self.init_window)
        self.pic_label.grid(row=3, column=1, rowspan=10, columnspan=5, sticky='NW')



def gui_start():
    # 实例化出一个父窗口
    init_window = Tk()
    tool = artName(init_window)
    # 设置根窗口默认属性
    tool.draw_window()
    # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示
    init_window.mainloop()


gui_start()
