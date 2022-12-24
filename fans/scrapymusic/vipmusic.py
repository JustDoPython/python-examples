import os
import tkinter as tk
import webbrowser
import requests
import tkinter.messagebox as mes_box
import PySimpleGUI as sg
from tkinter import ttk
from retrying import retry

​
class SetUI(object):
    """
    音乐弹框界面
    """

    def __init__(self, weight=1000, height=600):
        self.ui_weight = weight
        self.ui_height = height
        self.title = " 音乐破解软件"
        self.ui_root = tk.Tk(className=self.title)
        self.ui_url = tk.StringVar()
        self.ui_var = tk.IntVar()
        self.ui_var.set(1)
        self.show_result = None
        self.song_num = None
        self.response_data = None
        self.song_url = None
        self.song_name = None
        self.song_author = None

    def set_ui(self):
        """
        设置简易UI界面
        :return:
        """
        # Frame空间
        frame_1 = tk.Frame(self.ui_root)
        frame_2 = tk.Frame(self.ui_root)
        frame_3 = tk.Frame(self.ui_root)
        frame_4 = tk.Frame(self.ui_root)

        # ui界面中菜单设计
        ui_menu = tk.Menu(self.ui_root)
        self.ui_root.config(menu=ui_menu)
        file_menu = tk.Menu(ui_menu, tearoff=0)
        ui_menu.add_cascade(label='菜单', menu=file_menu)
        file_menu.add_command(label='使用说明', command=lambda: webbrowser.open('www.baidu.com'))
        file_menu.add_command(label='关于作者', command=lambda: webbrowser.open('www.baidu.com'))
        file_menu.add_command(label='退出', command=self.ui_root.quit)

        # 控件内容设置
        choice_passageway = tk.Label(frame_1, text='请选择音乐搜索通道：', padx=10, pady=10)
        passageway_button_1 = tk.Radiobutton(frame_1, text='酷我', variable=self.ui_var, value=1, width=10, height=3)
        passageway_button_2 = tk.Radiobutton(frame_1, text='网易云', variable=self.ui_var, value=2, width=10, height=3)
        passageway_button_3 = tk.Radiobutton(frame_1, text='QQ音乐', variable=self.ui_var, value=3, width=10, height=3)
        passageway_button_4 = tk.Radiobutton(frame_1, text='酷狗', variable=self.ui_var, value=4, width=10, height=3)
        input_link = tk.Label(frame_2, text="请输入歌曲名或歌手：")
        entry_style = tk.Entry(frame_2, textvariable=self.ui_url, highlightcolor='Fuchsia', highlightthickness=1,
                               width=35)
        label2 = tk.Label(frame_2, text=" ")
        play_button = tk.Button(frame_2, text="搜索", font=('楷体', 11), fg='Purple', width=2, height=1,
                                command=self.get_KuWoMusic)
        label3 = tk.Label(frame_2, text=" ")
        # 表格样式
        columns = ("序号", "歌手", "歌曲", "专辑")
        self.show_result = ttk.Treeview(frame_3, height=20, show="headings", columns=columns)
        # 下载
        download_button = tk.Button(frame_4, text="下载", font=('楷体', 11), fg='Purple', width=6, height=1, padx=5,
                                    pady=5, command=self.download_music)

        # 控件布局
        frame_1.pack()
        frame_2.pack()
        frame_3.pack()
        frame_4.pack()
        choice_passageway.grid(row=0, column=0)
        passageway_button_1.grid(row=0, column=1)
        passageway_button_2.grid(row=0, column=2)
        passageway_button_3.grid(row=0, column=3)
        passageway_button_4.grid(row=0, column=4)
        input_link.grid(row=0, column=0)
        entry_style.grid(row=0, column=1)
        label2.grid(row=0, column=2)
        play_button.grid(row=0, column=3, ipadx=10, ipady=10)
        label3.grid(row=0, column=4)
        self.show_result.grid(row=0, column=4)
        download_button.grid(row=0, column=5)

        # 设置表头
        self.show_result.heading("序号", text="序号")
        self.show_result.heading("歌手", text="歌手")
        self.show_result.heading("歌曲", text="歌曲")
        self.show_result.heading("专辑", text="专辑")
        # 设置列
        self.show_result.column("序号", width=100, anchor='center')
        self.show_result.column("歌手", width=200, anchor='center')
        self.show_result.column("歌曲", width=200, anchor='center')
        self.show_result.column("专辑", width=300, anchor='center')

        # 鼠标点击
        self.show_result.bind('<ButtonRelease-1>', self.get_song_url)

    @retry(stop_max_attempt_number=5)
    def get_KuWoMusic(self):
        """
        获取qq音乐
        :return:
        """
        # 清空treeview表格数据
        for item in self.show_result.get_children():
            self.show_result.delete(item)
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept - encoding': 'gzip, deflate',
            'accept - language': 'zh - CN, zh;q = 0.9',
            'cache - control': 'no - cache',
            'Connection': 'keep-alive',
            'csrf': 'HH3GHIQ0RYM',
            'Referer': 'http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6',
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/99.0.4844.51 Safari/537.36',
            'Cookie': '_ga=GA1.2.218753071.1648798611; _gid=GA1.2.144187149.1648798611; _gat=1; '
                      'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1648798611; '
                      'Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1648798611; kw_token=HH3GHIQ0RYM'
        }
        search_input = self.ui_url.get()
        if len(search_input) > 0:
            search_url = 'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?'
            search_data = {
                'key': search_input,
                'pn': '1',
                'rn': '80',
                'httpsStatus': '1',
                'reqId': '858597c1-b18e-11ec-83e4-9d53d2ff08ff'
            }
            try:
                self.response_data = requests.get(search_url, params=search_data, headers=headers, timeout=20).json()
                songs_data = self.response_data['data']['list']
                if int(self.response_data['data']['total']) <= 0:
                    mes_box.showerror(title='错误', message='搜索: {} 不存在.'.format(search_input))
                else:
                    for i in range(len(songs_data)):
                        self.show_result.insert('', i, values=(i + 1, songs_data[i]['artist'], songs_data[i]['name'],
                                                               songs_data[i]['album']))
            except TimeoutError:
                mes_box.showerror(title='错误', message='搜索超时，请重新输入后再搜索！')
        else:
            mes_box.showerror(title='错误', message='未输入需查询的歌曲或歌手，请输入后搜索！')

    def get_song_url(self, event):
        """
        获取下载歌曲的地址
        :return:
        """
        # treeview中的左键单击

        for item in self.show_result.selection():
            item_text = self.show_result.item(item, "values")
            # 获取
            print(1, item_text)
            self.song_num = int(item_text[0])
        # 获取下载歌曲的地址
        if self.song_num is not None:
            songs_data = self.response_data['data']['list']
            songs_req_id = self.response_data['reqId']
            song_rid = songs_data[self.song_num - 1]['rid']
            music_url = 'http://www.kuwo.cn/api/v1/www/music/playUrl?mid={}&type=convert_url3' \
                        '&httpsStatus=1&reqId={}' \
                .format(song_rid, songs_req_id)
            response_data = requests.get(music_url).json()
            self.song_url = response_data['data'].get('url')
            self.song_name = songs_data[self.song_num - 1]['name']
            self.song_author = songs_data[self.song_num - 1]['artist']
        else:
            mes_box.showerror(title='错误', message='未选择要下载的歌曲，请选择')

    def download_music(self):
        """
        下载音乐
        :return:
        """
        if not os.path.exists('./wangYiYun'):
            os.mkdir("./wangYiYun/")
        if self.song_num is not None:
            song_name = self.song_name + '--' + self.song_author + ".mp3"
            try:
                save_path = os.path.join('./wangYiYun/{}'.format(song_name)) \
                    .replace('\\', '/')
                true_path = os.path.abspath(save_path)
                resp = requests.get(self.song_url)
                with open(save_path, 'wb') as file:
                    file.write(resp.content)
                    mes_box.showinfo(title='下载成功', message='歌曲：%s,保存地址为%s' % (self.song_name, true_path))
            except Exception:
                mes_box.showerror(title='错误', message='未找到存放歌曲的文件夹')
        else:
            mes_box.showerror(title='错误', message='未选择要下载的歌曲，请选择后下载')

    def progress_bar(self, file_size):
        """
        任务加载进度条
        :return:
        """
        layout = [[sg.Text('任务完成进度')],
                  [sg.ProgressBar(file_size, orientation='h', size=(40, 20), key='progressbar')],
                  [sg.Cancel()]]

        # window只需将自定义的布局加载出来即可 第一个参数是窗口标题。
        window = sg.Window('机器人执行进度', layout)
        # 根据key值获取到进度条
        _progress_bar = window['progressbar']
        for i in range(file_size):  # 循环
            event, values = window.read(timeout=10)
            if event == 'Cancel' or event is None:
                break
            _progress_bar.UpdateBar(i + 1)

    def ui_center(self):
        """
        UI界面窗口设置：居中
        """
        ws = self.ui_root.winfo_screenwidth()
        hs = self.ui_root.winfo_screenheight()
        x = int((ws / 2) - (self.ui_weight / 2))
        y = int((hs / 2) - (self.ui_height / 2))
        self.ui_root.geometry('{}x{}+{}+{}'.format(self.ui_weight, self.ui_height, x, y))

    def loop(self):
        """
        函数说明:loop等待用户事件
        """
        self.ui_root.resizable(False, False)  # 禁止修改窗口大小
        self.ui_center()  # 窗口居中
        self.set_ui()
        self.ui_root.mainloop()


if __name__ == '__main__':
    a = SetUI()
    a.loop()