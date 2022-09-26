# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from scrapy.http.response.html import HtmlResponse

class DcdDownloaderMiddleware(object):

    def __init__(self):
        # 加载测试浏览器
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')

        self.driver = webdriver.Chrome(executable_path=r"C:\drf2\drf2\chromedriver.exe",options=options)
        self.driver.maximize_window()

    #重写process_request方法
    def process_request(self, request, spider):
        print('request.url',request.url)
        self.driver.get(request.url)
        js = 'return document.body.scrollHeight;'
        height = 0
        if request.url != 'https://www.dongchedi.com/auto/library/x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x':
            while True:
                new_height = self.driver.execute_script(js)
                if new_height > height:
                    self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                    height = new_height
                    time.sleep(1)
                else:
                    print("滚动条已经处于页面最下方!")
                    break
        source = self.driver.page_source
        # 创建一个response对象,把页面信息都封装在reponse对象中
        response = HtmlResponse(url=self.driver.current_url,body=source,request = request,encoding="utf-8")
        return response