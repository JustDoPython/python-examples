import requests
import json
import time
import random

cookies = "_uuid=033B11A7-07D4-2E24-3830-32A59DFACE2303106infoc; buvid3=675D7837-17AF-40C1-A04D-93ECD0C6B15813422infoc; rpdid=|(JYYk)|JJ|~0J'uYkllY~kmY; PVID=1; buvid_fp=675D7837-17AF-40C1-A04D-93ECD0C6B15813422infoc; buvid_fp_plain=675D7837-17AF-40C1-A04D-93ECD0C6B15813422infoc; CURRENT_QUALITY=0; SESSDATA=7df0deb3%2C1654955986%2C76995%2Ac1; bili_jct=074962e462340ac9cc2ae1673d906394; DedeUserID=10927197; DedeUserID__ckMd5=902c45cc54ce17cb; sid=agwcnv6j; i-wanna-go-back=1; b_ut=6; bp_t_offset_10927197=603736801110449695; CURRENT_FNVAL=2000; CURRENT_BLACKGAP=0; blackside_state=0; fingerprint=0dcd15d27d8afae5c38936e518ab5656; fingerprint3=aa0fd784f61f005b0c742ed5785e4b9b; fingerprint_s=29c59ad2325d7824a6f2c02bfbaf2838; innersign=0; b_lsid=F4E2AAC1_17DB8DCAF41; bsource=search_google"


def convert_cookies_to_dict(cookies):
    cookies = dict([l.split("=", 1) for l in cookies.split("; ")])
    return cookies

def getInfo(cookie):
    url = "http://api.bilibili.com/x/space/myinfo"

    

    resp = requests.get(url, cookies=cookie).text
    myinfo = json.loads(resp)

    data = myinfo['data']
    name = data['name']
    level_exp = data['level_exp']
    current_level = level_exp['current_exp']
    current_exp = level_exp['current_exp']
    next_exp = level_exp['next_exp']
    sub_exp = int(next_exp) - int(current_exp)
    days = int(sub_exp/70)
    coin = data['coins']
    print(data)
    print("{}，你的等级是{}，当前经验是{}，下一级经验是{}，还需要{}天升级，有{}个硬币".format(name, current_level,current_exp,next_exp,days,coin))

def getVideo(cookie):
    url = "http://api.bilibili.cn/recommend"

    resp = requests.get(url, cookies=cookie).text
    data = json.loads(resp)
    
    list_length = len(data['list'])
    result = []
    for i in range(list_length):
        data['list'][i]
        bvid = data['list'][i]['bvid']
        aid = data['list'][i]['aid']
        result.append({'bvid': bvid, 'aid': aid})
    return result

def view(bvid, aid, csrf):
    playedTime = random.randint(15, 100)
    url = "https://api.bilibili.com/x/click-interface/web/heartbeat"
    header = {
        "origin": "https://www.bilibili.com",
        "referer": "https://www.bilibili.com/video/"+bvid,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        "cookie": cookies

    }
    data = {
        'aid': aid,
        'bvid': bvid,
        'played_time': playedTime,
        'csrf': csrf
    }
    resp = requests.post(url, data = data ,headers=header).text
    json_data = json.loads(resp)
    code = json_data['code']
    if code == 0:
        print('视频观看成功，bvid 号为：' + bvid)
    else:
        print('视频观看失败，bvid 号为：' + bvid)

def coin(bvid, aid, csrf):
    
    url = "https://api.bilibili.com/x/web-interface/coin/add"
    data = {
        'aid': aid,
        'multiply': 1,
        'select_like': 1,
        'cross_domain': 'true',
        'csrf': csrf
    }
    header = {
        "origin": "https://www.bilibili.com",
        "referer": "https://www.bilibili.com/video/"+bvid,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        "cookie": cookies

    }

    resp = requests.post(url, headers=header, data=data).text
    data = json.loads(resp)
    code = data['code']
    if code == 0:
        print("投币成功")
    else:
        print('投币失败')


def share( bvid, csrf):
    url = 'https://api.bilibili.com/x/web-interface/share/add'
    data = {
        'csrf': csrf,
        'bvid': bvid
    }
    header = {
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        "Connection": "keep-alive",
        "origin": "https://t.bilibili.com",
        "referer": 'https://t.bilibili.com',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        "cookie": cookies

    }
    resp = requests.post(url, data=data, headers=header).text
    json_data = json.loads(resp)
    code = json_data['code']
    if code == 0:
        print('视频分享成功')
    else:
        print('视频分享失败')

if __name__ == '__main__':
    
    cookie = convert_cookies_to_dict(cookies)
    csrf = cookie['bili_jct']

    getInfo(cookie)
    
    data = getVideo(cookie)
    view(data[1]['bvid'], data[1]['aid'], csrf)
    
    for item in data:
        
        for i in range(6):
            coin(cookie,data[i]['bvid'], data[i]['aid'],csrf)
            time.sleep(5)
    
    share(data[1]['bvid'],data[1]['aid'], csrf)
