from time import sleep
import requests, urllib.request, re
import os, sys,json

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Cookie': 'SESSDATA=182cd036%2C1636985829%2C3b393%2A51',
        'Host': 'api.bilibili.com'
    }


Str = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'  # 准备的一串指定字符串
Dict = {}

# 将字符串的每一个字符放入字典一一对应 ， 如 f对应0 Z对应1 一次类推。
for i in range(58):
    Dict[Str[i]] = i

s = [11, 10, 3, 8, 4, 6, 2, 9, 5, 7]  # 必要的解密列表
xor = 177451812 
add = 100618342136696320  # 这串数字最后要被减去或加上

def algorithm_enc(av):
    ret = av
    av = int(av)
    av = (av ^ xor) + add
    # 将BV号的格式（BV + 10个字符） 转化成列表方便后面的操作
    r = list('BV          ')
    for i in range(10):
        r[s[i]] = Str[av // 58 ** i % 58]
    return ''.join(r)

def find_bid(p):
    bids = []
    r = requests.get(
            'https://api.bilibili.com/x/web-interface/newlist?&rid=20&type=0&pn={}&ps=50&jsonp=jsonp'.format(p))
      
    data = json.loads(r.text)
    archives = data['data']['archives']

    for item in archives:
        aid = item['aid']
        # r = requests.get('http://api.bilibili.com/x/web-interface/archive/stat?aid=' + str(aid), headers=headers)
        # bid = json.loads(r.text)['data']['bvid']
        bid = algorithm_enc(aid)
        bids.append(bid)

    return bids


def get_cid(bid):
    url = 'https://api.bilibili.com/x/player/pagelist?bvid=' + bid

    
    html = requests.get(url, headers=headers).json()

    infos = []

    data = html['data']
    cid_list = data
    for item in cid_list:
        cid = item['cid']
        title = item['part']
        infos.append({'bid': bid, 'cid': cid, 'title': title})
    return infos


# 访问API地址
def get_video_list(aid, cid, quality):
    url_api = 'https://api.bilibili.com/x/player/playurl?cid={}&bvid={}&qn={}'.format(cid, aid, quality)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Cookie': 'SESSDATA=182cd036%2C1636985829%2C3b393%2A51',
        'Host': 'api.bilibili.com'
    }
    html = requests.get(url_api, headers=headers).json()
    video_list = []

    for i in html['data']['durl']:
        video_list.append(i['url'])
    return video_list


# 下载视频

def schedule_cmd(blocknum, blocksize, totalsize):
    percent = 100.0 * blocknum * blocksize/ totalsize
    s = ('#' * round(percent)).ljust(100, '-')
    sys.stdout.write('%.2f%%' % percent + '[' + s + ']' + '\r')
    sys.stdout.flush()

#  下载视频
def download(video_list, title, bid):
    for i in video_list:
        opener = urllib.request.build_opener()
        # 请求头
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'),
            ('Accept', '*/*'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', 'gzip, deflate, br'), 
            ('Range', 'bytes=0-'),  
            ('Referer', 'https://www.bilibili.com/video/'+bid),
            ('Origin', 'https://www.bilibili.com'),
            ('Connection', 'keep-alive'),

        ]

        filename=os.path.join('D:\\video', r'{}_{}.mp4'.format(bid,title)) 

        try:
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(url=i, filename=filename, reporthook=schedule_cmd) 
        except:
            print(bid + "下载异常，文件：" + filename)

if __name__ == '__main__':
    # algorithm_enc(545821176)
    bids = find_bid(1)
    print(len(bids))
    for bid in bids:
        sleep(10)
        cid_list = get_cid(bid)

        for item in cid_list:
            cid = item['cid']
            title = item['title']
            title = re.sub(r'[\/\\:*?"<>|]', '', title)  # 替换为空的
            bid = item['bid']
            video_list = get_video_list(bid, cid, 80)
        
            download(video_list, title, bid)
