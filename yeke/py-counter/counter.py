import re
import tkinter
import tkinter.messagebox

# 点击事件
def onclick(btn):
    # 运算符
    operation = ('+', '-', '*', '/', '**', '//')
    # 获取文本框中的内容
    content = contentVar.get()
    # 如果已有内容是以小数点开头的，在前面加 0
    if content.startswith('.'):
        content = '0' + content  # 字符串可以直接用+来增加字符
    # 根据不同的按钮作出不同的反应
    if btn in '0123456789':
        # 按下 0-9 在 content 中追加
        content += btn
    elif btn == '.':
        # 将 content 从 +-*/ 这些字符的地方分割开来
        lastPart = re.split(r'\+|-|\*|/', content)[-1]
        if '.' in lastPart:
            # 信息提示对话框
            tkinter.messagebox.showerror('错误', '重复出现的小数点')
            return
        else:
            content += btn
    elif btn == 'C':
        # 清除文本框
        content = ''
    elif btn == '=':
        try:
            # 对输入的表达式求值
            content = str(eval(content))
        except:
            tkinter.messagebox.showerror('错误', '表达式有误')
            return
    elif btn in operation:
        if content.endswith(operation):
            tkinter.messagebox.showerror('错误', '不允许存在连续运算符')
            return
        content += btn
    elif btn == '√':
        # 从 . 处分割存入 n，n 是一个列表
        n = content.split('.')
        # 如果列表中所有的都是数字，就是为了检查表达式是不是正确的
        if all(map(lambda x: x.isdigit(), n)):
            content = eval(content) ** 0.5
        else:
            tkinter.messagebox.showerror('错误', '表达式错误')
            return
    # 将结果显示到文本框中
    contentVar.set(content)

# 创建主窗口
tk = tkinter.Tk()
# 设置窗口大小和位置
tk.geometry('300x210+500+200')
# 不允许改变窗口大小
tk.resizable(False, False)
# 设置窗口标题
tk.title('计算器')
# 自动刷新字符串变量，可用 set 和 get 方法进行传值和取值
contentVar = tkinter.StringVar(tk, '')
# 创建单行文本框
contentEntry = tkinter.Entry(tk, textvariable=contentVar)
# 设置文本框为只读
contentEntry['state'] = 'readonly'
# 设置文本框坐标及宽高
contentEntry.place(x=20, y=10, width=260, height=30)
# 按钮显示内容
bvalue = ['C', '+', '-', '//', '2', '0', '1', '√', '3', '4', '5', '*', '6', '7', '8', '.', '9', '/', '**', '=']
index = 0
# 将按钮进行 5x4 放置
for row in range(5):
    for col in range(4):
        d = bvalue[index]
        index += 1
        btnDigit = tkinter.Button(tk, text=d, command=lambda x=d: onclick(x))
        btnDigit.place(x=20 + col * 70, y=50 + row * 30, width=50, height=20)
# 进入消息循环
tk.mainloop()