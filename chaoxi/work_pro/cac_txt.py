#coding:utf-8
import re
#读取目标文本文件
def get_str(path):
    f = open(path)
    data = f.read()
    f.close()
    return data
# 输入目标路径
path=input("请输入文件路径：")

word=re.findall('([\u4e00-\u9fa5])',get_str(path))

# 计算出特殊字符外的字数
print("中文字符,除特殊字符外共：",len(word))