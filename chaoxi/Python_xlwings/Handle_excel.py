import xlwings as xw
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# 打开已保存的 Excel
def open_excel():
     file_path = r'G:/test/test.xlsx'

     wb = xw.Book(file_path)  # 固定打开表格
    # xw.books.open(file_path)  # 频繁打开表格

    # 引用表空间
     sht = wb.sheets['sheet1']

    # 引用单元格
     rng = xw.Range('A1')
    # rng = sht['a1']
    # rng = sht[0,0] 第一行的第一列即a1,相当于pandas的切片

    # 引用区域
    # rng = sht.range('a1:a5')
    # rng = sht['a1:a5']
    # rng = sht[:5,0]

     xw.Book(file_path).sheets[0].range('A1:D5')

    # 写入数据
     sht.range('A1').value = 'Hello Excel'

     sht.range('A1').value = [1, 2, 3, 4, 5, 6, 7, 8]

    # 按照列写入数据
     sht.range('A2').options(transpose=True).value = [2, 3, 4, 5, 6, 7, 8]

    # 二维列表写入数据
     sht.range('A9').expand('table').value = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'], ['j', 'k', 'l']]

     print(sht.range('A1:D5').value)

     wb.save()

#def read_data():

if __name__ == '__main__':
    #open_excel()

    fig = plt.figure()  # 指定画布
    # plt.plot([1, 2, 3, 4, 5])
    plt.plot([36,5,3,25,78])
    plt.plot([9,10,31,45])
    plt.plot([6,14,45,31])
    sht = xw.Book(r'G:/test/test.xlsx').sheets[0]
    sht.pictures.add(fig, name='myplt', update=True)