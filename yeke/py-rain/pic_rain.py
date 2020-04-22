from tkinter import *
import random, threading, time, os

# 初始雨滴纵坐标
INIT_HEIGHT = 10
# 雨滴创建
def rainmake(canvas, imagefile):
    rainlist = []
    for i in range(5):
        # 根据图片，创建一排福字
        rainlist.append(canvas.create_image(100 + 80 * i, INIT_HEIGHT, anchor=NE, image=imagefile))
    return rainlist

# 雨滴下落
def raindown(tk, canvas, imagefile, sec):
    # 线程间等待
    time.sleep(sec)
    rainlist = rainmake(canvas, imagefile)
    # 每个福字的纵坐标值
    height = [INIT_HEIGHT] * 10
    while True:
        # 每次移动前稍等一会
        time.sleep(0.2)
        # 5 个福字一起移动
        for i in range(5):
            # 如果福字到底了，则不继续移动
            if not height[i] == 0:
                # 设置下落步调
                rnd = random.randint(5, 50)
                canvas.move(rainlist[i], 0, rnd)
                height[i] = height[i] + rnd
                tk.update()
        for i,h in enumerate(height):
            if h > 400:
                # 当福字走到最下方，则删除
                canvas.delete(rainlist[i])
                tk.update()
                # 清空该福的 height
                height[i] = 0
                print(i,h,height)
        # 全到底，则跳出循环
        if height == [0] * 5:
            print('break:',threading.current_thread().name)
            break

def lookloop(tk, canvas, thread):
    aliveflg = False
    while True:
        # 5s 检测一次
        time.sleep(5)
        for th in thread:
            if th.is_alive():
                aliveflg = True
            else:
                aliveflg = False
        if aliveflg == False:
            break
    canvas.create_text(100 , 200, text='雨停了...', fill='red')
    canvas.pack()
    time.sleep(5)
    tk.destroy()

def main():
    # 创建窗口对象
    tk = Tk()
    tk.title('送福雨')
    canvas_style = {
        'bg':'white',
        'height':'500',
        'width':'410',
        'cursor':'circle'
    }
    # 创建画布
    canvas = Canvas(tk,canvas_style)
    canvas.pack()
    # 图片素材
    if not os.path.exists('pic.gif'):
        raise Exception('pic.gif file does not exists.')
    imagefile = PhotoImage(file = 'pic.gif')
    thread = []
    for i in range(100):
       thread.append(threading.Thread(target=raindown, args=(tk, canvas, imagefile, i)))
    for t in thread:
        t.start()
        # 新开一个线程监控运行中的线程
    threading.Thread(target=lookloop, args=(tk, canvas, thread)).start()
    # 进入消息循环
    tk.mainloop()

if __name__ == '__main__':
    main()