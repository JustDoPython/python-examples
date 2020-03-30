# 引入模块
import requests
import json
import re
import time
from bs4 import BeautifulSoup
import os

#保存下载的 html 页面和图片
def save(search_response,html_dir,file_name):
    # 保存 html 的位置
    htmlDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), html_dir)
    # 保存图片的位置
    targetDir = os.path.join(os.path.dirname(os.path.abspath(__file__)),html_dir + '/images')
    # 不存在创建文件夹
    if not os.path.isdir(targetDir):
        os.makedirs(targetDir)
    domain = 'https://mp.weixin.qq.com/s'
    # 调用保存 html 方法
    save_html(search_response, htmlDir, file_name)
    # 调用保存图片方法
    save_file_to_local(htmlDir, targetDir, search_response, domain, file_name)

# 保存图片到本地
def save_file_to_local(htmlDir,targetDir,search_response,domain,file_name):
    # 使用lxml解析请求返回的页面
    obj = BeautifulSoup(save_html(search_response,htmlDir,file_name).content, 'lxml')  
    # 找到有 img 标签的内容
    imgs = obj.find_all('img')
    # 将页面上图片的链接加入list
    urls = []
    for img in imgs:
        if 'data-src' in str(img):
            urls.append(img['data-src'])
        elif 'src=""' in str(img):
            pass
        elif "src" not in str(img):
            pass
        else:
            urls.append(img['src'])

    # 遍历所有图片链接，将图片保存到本地指定文件夹，图片名字用0，1，2...
    i = 0
    for each_url in urls:
        # 跟据文章的图片格式进行处理
        if each_url.startswith('//'):
            new_url = 'https:' + each_url
            r_pic = requests.get(new_url)
        elif each_url.startswith('/') and each_url.endswith('gif'):
            new_url = domain + each_url
            r_pic = requests.get(new_url)
        elif each_url.endswith('png') or each_url.endswith('jpg') or each_url.endswith('gif') or each_url.endswith('jpeg'):
            r_pic = requests.get(each_url)
        # 创建指定目录
        t = os.path.join(targetDir, str(i) + '.jpeg')
        print('该文章共需处理' + str(len(urls)) + '张图片，正在处理第' + str(i + 1) + '张……')
        # 指定绝对路径
        fw = open(t, 'wb')
        # 保存图片到本地指定目录
        fw.write(r_pic.content)
        i += 1
        # 将旧的链接或相对链接修改为直接访问本地图片
        update_file(each_url, t, htmlDir, file_name)
        fw.close()

# 保存 HTML 到本地
def save_html(url_content,htmlDir,file_name):
    f = open(htmlDir+"/"+file_name+'.html', 'wb')
    # 写入文件
    f.write(url_content.content)
    f.close()
    return url_content

# 修改 HTML 文件,将图片的路径改为本地的路径
def update_file(old, new, htmlDir, file_name):
        # 打开两个文件，原始文件用来读，另一个文件将修改的内容写入
    with open(htmlDir+"/"+file_name+'.html', encoding='utf-8') as f, open(htmlDir+"/"+file_name+'_bak.html', 'w', encoding='utf-8') as fw:
        # 遍历每行，用replace()方法替换路径
        for line in f:
            new_line = line.replace(old, new)
            new_line = new_line.replace("data-src", "src")
                # 写入新文件
            fw.write(new_line)
    # 执行完，删除原始文件
    os.remove(htmlDir+"/"+file_name+'.html')
    time.sleep(5)
    # 修改新文件名为 html
    os.rename(htmlDir+"/"+file_name+'_bak.html', htmlDir+"/"+file_name+'.html')

# 打开 cookie.txt
with open("cookie.txt", "r") as file:
    cookie = file.read()
cookies = json.loads(cookie)
url = "https://mp.weixin.qq.com"
#请求公号平台
response = requests.get(url, cookies=cookies)
# 从url中获取token
token = re.findall(r'token=(\d+)', str(response.url))[0]
# 设置请求访问头信息
headers = {
    "Referer": "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=" + token + "&lang=zh_CN",
    "Host": "mp.weixin.qq.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
}

# 循环遍历前10页的文章
for j in range(1, 10, 1):
    begin = (j-1)*5
    # 请求当前页获取文章列表
    requestUrl = "https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin="+str(begin)+"&count=5&fakeid=MzU1NDk2MzQyNg==&type=9&query=&token=" + token + "&lang=zh_CN&f=json&ajax=1"
    search_response = requests.get(requestUrl, cookies=cookies, headers=headers)
    # 获取到返回列表 Json 信息
    re_text = search_response.json()
    list = re_text.get("app_msg_list")
    # 遍历当前页的文章列表
    for i in list:
        # 目录名为标题名，目录下存放 html 和图片
        dir_name = i["title"].replace(' ','')
        print("正在下载文章：" + dir_name)
        # 请求文章的 url ，获取文章内容
        response = requests.get(i["link"], cookies=cookies, headers=headers)
        # 保存文章到本地
        save(response, dir_name, i["aid"])
        print(dir_name + "下载完成!")
    # 过快请求可能会被微信问候，这里进行10秒等待
    time.sleep(10)


