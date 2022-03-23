# coding:utf-8

import sys
import requests


def response(flow):
    url = flow.request.url
    content_type = flow.response.headers.get('Content-Type', default=None)
    print(content_type)
    if "finder.video.qq.com" in url:
        content_type = flow.response.headers.get('Content-Type', default=None)
        if content_type is not None and content_type == 'video/mp4':
            print(url)
            file_name = './urls.txt'
            with open(file_name, mode='a', encoding='utf-8') as f:
                f.write(url)
                f.write('\n')
                f.close()
