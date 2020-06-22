import base64
import os

import subprocess
import time
import requests
from pyecharts.charts import Bar, Pie
from pyecharts import options as opts

class zhubo():

    mobile_root = "/sdcard/zhubo/"
    computer_root = "/Users/xx/Desktop/zhubo/"
    except_file = "/Users/xx/Desktop/zhubo/except.txt"


    def __init__(self):
        '''
        查看连接的手机，没有手机连接则抛出异常
        '''

        connect = subprocess.Popen("adb devices",
                                   stderr=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   shell=True)
        stdout, stderr = connect.communicate()  # 获取返回命令
        # 输出执行命令结果结果
        stdout = stdout.decode("utf-8")

        if len(stdout) <= 26:
            raise Exception("没有连接到手机")
        print("成功连接手机!")


    def screen(self, platform):
        '''
        截取屏幕，保存到手机中的 /sdcard/zhubo/platform 文件夹中
        :param platform: 平台，如：taobao、pdd、jingdong
        '''

        for i in range(1, 618):
            time.sleep(3)
            pic_name = platform + '_' + str(int(time.time() * 1000)) + '.png'

            # 截屏
            screencap = subprocess.Popen('adb shell /system/bin/screencap -p ' + self.mobile_root + platform + '/' + pic_name,
                                       stderr=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       shell=True)

            # 滑动屏幕
            swipe = subprocess.Popen('adb shell input swipe 1000 300 1000 10',
                                       stderr=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       shell=True)
            print(str(i) + '    ' + pic_name)


    def pull(self, platform):
        '''
        发送到电脑
        '''

        # 列出所有图像
        connect = subprocess.Popen('adb shell ls ' + self.mobile_root + platform,
                                   stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        stdout, stderr = connect.communicate()
        stdout = stdout.decode("utf-8")
        pics = stdout.split('\n')

        for pic_name in pics:
            # 发送到电脑 /Users/xx/Desktop/zhubo/platform 文件夹下
            connect = subprocess.Popen('adb pull' + self.mobile_root + platform + '/' + pic_name  + ' ' + self.computer_root + platform + '/' + pic_name,
                                        stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        print('手机中的图像成功发送到电脑')

    def getAccessToken(self):
        '''
        获取百度 AI 开放平台的 access_token
        :return: access_token
        '''

        ak = 'ak'
        sk = 'sk'

        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + ak + '&client_secret=' + sk
        response = requests.get(host)
        if response:
            return response.json()['access_token']

    def image2base64(self, pic_path):
        '''
        图片转base64
        :param image_path: 图片地址
        :return: base64
        '''

        with open(pic_path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            s = base64_data.decode()
            return s

    def beauty_detect(self, access_token, platform):
        '''
        人脸检测
        :param access_token: access_token
        :param platform: 平台，如：taobao、pdd、jingdong
        :return: 文件
        '''

        # 人脸检测 url
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"

        # 为了防止请求百度发生意外事故，将颜值结果写入文件
        filename = self.computer_root + platform + '.txt'

        index = 0
        # 循环所有图片
        for root, dirs, files in os.walk(self.computer_root + platform ):
            for pic in files:
                index = index + 1
                base64img = self.image2base64(root + '/' + pic)

                params = "{\"image\":\"" + base64img + "\",\"image_type\":\"BASE64\",\"face_field\":\"beauty\"}"
                request_url = request_url + "?access_token=" + access_token
                headers = {'content-type': 'application/json'}

                # 免费 API QPS只有2个，可以使用多个账号，注意:这里容易异常
                response = requests.post(request_url, data=params, headers=headers)

                print(response)
                if response:
                    json = response.json()
                    print(json)
                    # 解析获取颜值i
                    if json['error_msg'] == 'SUCCESS':
                        face_list = json['result']['face_list']
                        beauty_list = []
                        for face in face_list:
                            beauty_list.append(face['beauty'])
                            beauty = max(beauty_list)

                            with open(filename, 'a') as f:
                                f.write(str(index) + ',' + pic + ',' + str(beauty) + '\n')
                                print(str(index) + ',' + pic + ',' + str(beauty) + '\n')


    def calc(self, platform):
        '''
        统计颜值区间的个数
        :param platform: 平台，如：taobao、pdd、douyin
        :return: 颜值区间汇总、颜值字典
        '''

        beauty_sum_dir = {"90-100": 0, "80-89": 0, "70-79": 0, "60-69": 0, "50-59": 0, "40-49": 0, "30-39": 0,
                          "20-29": 0, "10-19": 0, "0-9": 0}
        beauty_dir = {}

        beauty_areas = ["90-100", "80-89", "70-79", "60-69", "50-59", "40-49", "30-39", "20-29", "10-19", "0-9"]

        filename =  self.computer_root + platform + '.txt'

        with open(filename) as f:
            lines = f.readlines()

        if lines == None or len(lines) == 0:
            raise Exception(filename + '中没有颜值数据')


        index = 0
        for line in lines:
            # 只取 618 个图像
            index = index + 1
            if index > 618:
                break

            l = line.rstrip()
            result = l.split(',')
            beauty = float(result[2])

            beauty_area = beauty_areas[int((beauty // 10 * -1) - 1)]
            beauty_sum_dir[beauty_area] = beauty_sum_dir.get(beauty_area) + 1

            beauty_dir[result[1]] = result[2]

        return beauty_sum_dir, beauty_dir

    def bar(self, taobao_beauty_sum_dir = {}, pdd_beauty_sum_dir = {}, douyin_beauty_sum_dir = {}):
        '''
        柱状图
        :param taobao_beauty_sum_dir: 淘宝颜值区间汇总
        :param pdd_beauty_sum_dir: 拼多多颜值区间汇总
        :param douyin_beauty_sum_dir: 抖音颜值区间汇总
        :return:
        '''

        bar = (
            Bar()
                .add_xaxis(list(taobao_beauty_sum_dir.keys()))
                .add_yaxis('淘宝', list(taobao_beauty_sum_dir.values()))
                .add_yaxis("拼多多", list(pdd_beauty_sum_dir.values()))
                .add_yaxis("抖音", list(douyin_beauty_sum_dir.values()))
                .set_global_opts(title_opts=opts.TitleOpts(title="主播颜值柱状图"))

        )
        bar.render("颜值柱状图.html")

    def pie(self, platform, beauty_sum_dir = {}):
        '''
        饼图
        :param platform:  平台，如：taobao、pdd、douyin
        :param beauty_sum_dir: 颜值区间汇总
        :return:
        '''

        c = (
            Pie()
                .add(
                "",
                [list(z) for z in zip(beauty_sum_dir.keys(), beauty_sum_dir.values())],
                center=["35%", "50%"],
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title=platform + '主播颜值饼图'),
                legend_opts=opts.LegendOpts(pos_left="15%"),
            )
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}（{d}%）"))
                .render(platform + "颜值饼图.html")
        )

    def sorted_by_value(self, beauty_dir):
        beauty_sorted = sorted(beauty_dir.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
        print(beauty_sorted)
        return beauty_sorted




if __name__ == '__main__':
    a = zhubo()
    a.screen('pdd')
    a.pull('pdd')
    access_token = a.getAccessToken()

    platforms = ['taobao', 'pdd', 'douyin']
    for platform in platforms:
        a.beauty_detect(access_token, 'taobao')


    taobao_beauty_sum_dir, taobao_beauty_dir = a.calc('taobao')
    pdd_beauty_sum_dir, pdd_beauty_dir = a.calc('pdd')
    douyin_beauty_sum_dir, douyin_beauty_dir = a.calc('douyin')

    # 图表
    a.bar(taobao_beauty_sum_dir,pdd_beauty_sum_dir,douyin_beauty_sum_dir)
    a.pie('淘宝', taobao_beauty_sum_dir)
    a.pie('拼多多', pdd_beauty_sum_dir)
    a.pie('抖音', douyin_beauty_sum_dir)
    taobao_beauty_dir.update(douyin_beauty_dir)
    taobao_beauty_dir.update(pdd_beauty_dir)
    a.sorted_by_value(taobao_beauty_dir)