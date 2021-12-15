
import os
import requests,re


def get_html(search_key, page):
    header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Host': 'www.fabiaoqing.com'
        }

    key_url = 'https://fabiaoqing.com/search/bqb/keyword/{}/type/bq/page/{}.html'.format(search_key, page)

    resp = requests.get(key_url, headers=header)
    resp.encoding='utf-8'
    return resp.text

def get_src(html):
    srcs = re.findall('<img class="ui image bqppsearch lazy" data-original="(.*?)" src="(.*?)" title="(.*?)"',html,re.S)
    return srcs

def downlaod(srcs, path):
    
    from urllib.request import urlretrieve
    for item in srcs:
        print(item[2])
        urlretrieve(item[0], path + '\\' + item[2].replace('\n', '') + '.png')


if __name__=="__main__":
    search_key = input("请输入需要的表情包：") 

    path = "D:\image\{}".format(search_key); 

    try:
        os.makedirs(path)
    except:
        pass

    for i in range(5):
        html = get_html(search_key, i)
        srcs = get_src(html)
        if len(srcs) == 0:
            print("已经没有表情包了，下载完成了")
        downlaod(srcs, path)
