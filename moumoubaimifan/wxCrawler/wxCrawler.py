# coding:utf-8
# wxCrawler.py
import os
import time

import requests
import json
import urllib3

import utils
from articles import Articles


class WxCrawler(object):
    """翻页内容抓取"""
    urllib3.disable_warnings()

    def __init__(self, appmsg_token, biz, cookie, begin_page_index = 0, end_page_index = 100):
        # 起始页数
        self.begin_page_index = begin_page_index
        # 结束页数
        self.end_page_index = end_page_index
        # 抓了多少条了
        self.num = 1

        self.appmsg_token = appmsg_token
        self.biz = biz
        self.headers = {
            "User-Agent": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0Chrome/57.0.2987.132 MQQBrowser/6.2 Mobile",
            "Cookie": cookie
        }
        self.cookie = cookie

    def article_list(self, context):
        articles = json.loads(context).get('general_msg_list')
        return json.loads(articles)

    def run(self):

        # 翻页地址
        page_url = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz={}&f=json&offset={}&count=10&is_ok=1&scene=&uin=777&key=777&pass_ticket={}&wxtoken=&appmsg_token=" + self.appmsg_token + "&x5=0f=json"
        # 将 cookie 字典化
        wx_dict = utils.str_to_dict(self.cookie, join_symbol='; ', split_symbol='=')
        # 请求地址
        response = requests.get(page_url.format(self.biz, self.begin_page_index * 10, wx_dict['pass_ticket']), headers=self.headers, verify=False)
        # 将文章列表字典化
        articles = self.article_list(response.text)
        info = Articles(self.appmsg_token, self.cookie)

        result = []
        for a in articles['list']:
            if 'app_msg_ext_info' in a.keys() and '' != a.get('app_msg_ext_info').get('content_url', ''):

                read_num, old_like_num, like_num = info.read_like_nums(a.get('app_msg_ext_info').get('content_url'))
                result.append(str(self.num) + '条,' + a.get('app_msg_ext_info').get('title') + ',' + str(read_num) + ',' + str(old_like_num) + ',' + str(like_num))
                time.sleep(2)

            if 'app_msg_ext_info' in a.keys():
                for m in a.get('app_msg_ext_info').get('multi_app_msg_item_list', []):
                    read_num, old_like_num, like_num = info.read_like_nums(m.get('content_url'))
                    result.append(str(self.num) + '条的副条,' + m.get('title') + ',' + str(read_num) + ',' + str(old_like_num) + ',' + str(like_num))

                    time.sleep(3)

            self.num = self.num + 1

        self.write_file(result)

        self.is_exit_or_continue()
        # 递归调用
        self.run()

    def write_file(self, result):
        with open('微信公众号.csv', 'a') as f:
            for row in result:
                f.write(row + '\n')

    def is_exit_or_continue(self):
        self.begin_page_index = self.begin_page_index + 1

        if self.begin_page_index > self.end_page_index:
            print('公众号导出结束，共导出了' + str(self.end_page_index) + '页')
            os.exit()
