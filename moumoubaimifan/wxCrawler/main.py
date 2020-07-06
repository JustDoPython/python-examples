# coding:utf-8
# main.py
from read_cookie import ReadCookie
from wxCrawler import WxCrawler

"""程序启动类"""
if __name__ == '__main__':
    cookie = ReadCookie('E:/python/cookie.txt')

    cookie.write_cookie()
    appmsg_token, biz, cookie_str = cookie.parse_cookie()
    wx = WxCrawler(appmsg_token, biz, cookie_str)
    wx.run()
