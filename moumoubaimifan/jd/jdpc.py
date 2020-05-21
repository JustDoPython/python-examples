import requests
import random
import time
import os
import json

from PIL import Image

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'

session = requests.session()


def show_QRcode():
    url = 'https://qr.m.jd.com/show'
    params = {
        'appid': 133,
        'size': 147,
        't': str(int(time.time() * 1000)),
    }
    headers = {
        'User-Agent': user_agent,
        'Referer': 'https://passport.jd.com/new/login.aspx',
    }
    resp = session.get(url=url, headers=headers, params=params)

    QRcode_path = 'QRcode.png'
    with open(QRcode_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024):
            f.write(chunk)

    QRcode = Image.open(QRcode_path)
    QRcode.show()

def check_QRcode():
    
    url = 'https://qr.m.jd.com/check'
    params = {
        'appid': '133',
        'callback': 'jQuery{}'.format(random.randint(1000000, 9999999)),
        'token': session.cookies.get('wlfstk_smdl'),
        '_': str(int(time.time() * 1000)),
    }
    headers = {
        'User-Agent': user_agent,
        'Referer': 'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F',
    }
    resp = session.get(url=url, headers=headers, params=params)
    resp_json = parse_json(resp.text)

    if 'ticket' in resp_json:
        print(resp_json)
        return resp_json['ticket']
    else:
        print(resp_json['msg'])
        print('请刷新JD登录二维码！')
        os._exit(0)


def validation_QRcode(ticket):

    url = 'https://passport.jd.com/uc/qrCodeTicketValidation'
    headers = {
        'User-Agent': user_agent,
        'Referer': 'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F',
    }
    params={
        't': ticket
    }
    resp = session.get(url=url, headers=headers, params=params)
    print(resp.text)


def parse_json(str):
    return json.loads(str[str.find('{'):str.rfind('}') + 1])


def coupon_list():
    url = 'https://a.jd.com/indexAjax/getCouponListByCatalogId.html'
    headers = {
        'User-Agent': user_agent,
        'Referer': 'https://a.jd.com/?cateId=118',
    }
    couponList = []
    for i in range(1, 20):
        params = {
            'callback': 'jQuery{}'.format(random.randint(1000000, 9999999)),
            'catalogId': '118',
            'page': str(i),
            'pageSize': '9',
            '_': str(int(time.time() * 1000)),
        }
        try:
            resp = session.get(url=url, params=params, headers=headers)
            json = parse_json(resp.text)
            couponList.extend(json['couponList'])
            if json['totalNum'] == 1:
                continue
            else:
                break
        except Exception:
            print('出错了!')
    return couponList


def get_coupon(coupon_list):
    url = 'https://a.jd.com/indexAjax/getCoupon.html'
    headers = {
        'User-Agent': user_agent,
        'Referer': 'https://a.jd.com/?cateId=118',
    }
    for coupon in coupon_list:
        params = {
            'callback': 'jQuery{}'.format(random.randint(1000000, 9999999)),
            'key': coupon['key'],
            'type': '1',
            '_': str(int(time.time() * 1000)),
        }
        time.sleep(1)
        resp = session.get(url=url, params=params, headers=headers)
        print(resp.text)



if __name__ == '__main__':
    show_QRcode()

    time.sleep(10)

    ticket = check_QRcode()
    validation_QRcode(ticket)
    coupon_list = coupon_list()
    get_coupon(coupon_list)