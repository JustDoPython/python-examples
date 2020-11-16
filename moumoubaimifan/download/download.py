# coding=utf-8
import os
from urllib import request

import requests
import urllib3

import wget
from tqdm import tqdm

url = 'https://cn.bing.com/th?id=OHR.DerwentIsle_EN-CN8738104578_400x240.jpg'

def requests_download():

    content = requests.get(url).content

    with open('pic_requests.jpg', 'wb') as file:
        file.write(content)

def urllib_download():
    request.urlretrieve(url, 'pic_urllib.jpg')


def urllib3_download():
    # 创建一个连接池
    poolManager = urllib3.PoolManager()

    resp = poolManager.request('GET', url)
    with open("pic_urllib3.jpg", "wb") as file:
        file.write(resp.data)

    resp.release_conn()


def wget_download():
    wget.download(url, out='pic_wget.jpg')

def steam_download():
    url = 'https://vscode.cdn.azure.cn/stable/e5a624b788d92b8d34d1392e4c4d9789406efe8f/VSCodeUserSetup-x64-1.51.1.exe'

    with requests.get(url, stream=True) as r:
        with open('vscode.exe', 'wb') as flie:
            # chunk_size 指定写入大小每次写入 1024 * 1024 bytes
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    flie.write(chunk)

def tqdm_download():
    url = 'https://vscode.cdn.azure.cn/stable/e5a624b788d92b8d34d1392e4c4d9789406efe8f/VSCodeUserSetup-x64-1.51.1.exe'

    resp = requests.get(url, stream=True)

    # 获取文件大小
    file_size = int(resp.headers['content-length'])

    with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024, ascii=True, desc='vscode.exe') as bar:
        with requests.get(url, stream=True) as r:
            with open('vscode.exe', 'wb') as fp:
                for chunk in r.iter_content(chunk_size=512):
                    if chunk:
                        fp.write(chunk)
                        bar.update(len(chunk))

def duan_download():
    url = 'https://vscode.cdn.azure.cn/stable/e5a624b788d92b8d34d1392e4c4d9789406efe8f/VSCodeUserSetup-x64-1.51.1.exe'

    r = requests.get(url, stream=True)

    # 获取文件大小
    file_size = int(r.headers['content-length'])

    file_name = 'vscode.exe'
    # 如果文件存在获取文件大小，否在从 0 开始下载，
    first_byte = 0
    if os.path.exists(file_name):
        first_byte = os.path.getsize(file_name)

    # 判断是否已经下载完成
    if first_byte >= file_size:
        return

    # Range 加入请求头
    header = {"Range": f"bytes={first_byte}-{file_size}"}

    # 加了一个 initial 参数
    with tqdm(total=file_size, unit='B', initial=first_byte, unit_scale=True, unit_divisor=1024, ascii=True, desc=file_name) as bar:
        # 加 headers 参数
        with requests.get(url, headers = header, stream=True) as r:
            with open(file_name, 'ab') as fp:
                for chunk in r.iter_content(chunk_size=512):
                    if chunk:
                        fp.write(chunk)
                        bar.update(len(chunk))


if __name__ == '__main__':
    duan_download()
