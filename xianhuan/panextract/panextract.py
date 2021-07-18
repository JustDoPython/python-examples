#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作者：闲欢  公众号：Python技术

from tkinter import *

# str = '链接: https://pan.baidu.com/s/1ctcXiZymWst2NC_JPDkr4Q 提取码: j1ub 复制这段内容后打开百度网盘手机App，操作更方便哦'
class panTool:
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    def extractData(self):
        str = self.init_data_text.get(1.0, END)
        url_pattern = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        code_pattern = '(?<=提取码: )[0-9a-z]{4}'
        url_regex = re.compile(url_pattern)
        code_regex = re.compile(code_pattern)
        # 输出到界面
        self.link_data_text.delete(1.0, END)
        self.code_data_text.delete(1.0, END)
        self.link_data_text.insert(1.0, url_regex.findall(str)[0])
        self.code_data_text.insert(1.0, code_regex.findall(str)[0])
        return

    def draw_window(self):
        self.init_window = Tk()  # 实例化出一个父窗口
        self.init_window.title("百度网盘提取链接工具_v1.0")  # 窗口名
        self.init_window.geometry('800x300+10+10')
        # 源信息
        self.init_data_label = Label(self.init_window, text="复制的提取信息")
        self.init_data_label.grid(row=0, column=0)
        self.init_data_text = Text(self.init_window, width=100, height=5, borderwidth=1, relief="solid")  # 原始数据录入框
        self.init_data_text.grid(row=1, column=0, columnspan=10)

        # 按钮
        self.str_trans_button = Button(self.init_window, text="提取", width=10, height=2, bg="blue",
                                       command=self.extractData)  # 调用内部方法  加()为直接调用
        self.str_trans_button.grid(row=2, column=2)

        # 链接
        self.link_data_label = Label(self.init_window, width=10, text="链接")
        self.link_data_label.grid(row=3, column=0, columnspan=1)
        self.link_data_text = Text(self.init_window, width=60, height=2, borderwidth=1, relief="solid")
        self.link_data_text.grid(row=3, column=1, columnspan=6)

        # 提取码
        self.code_data_label = Label(self.init_window, width=10, text="提取码")
        self.code_data_label.grid(row=3, column=7, columnspan=1)
        self.code_data_text = Text(self.init_window, width=20, height=2, borderwidth=1, relief="solid")
        self.code_data_text.grid(row=3, column=8, columnspan=2)

def gui_start():
    # 实例化出一个父窗口
    init_window = Tk()
    tool = panTool(init_window)
    # 设置根窗口默认属性
    tool.draw_window()
    # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示
    init_window.mainloop()

gui_start()

