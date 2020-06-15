import re

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
    session.get(url=url, headers=headers, params=params)


def parse_json(str):
    try:
        return json.loads(str[str.find('{'):str.rfind('}') + 1])
    except:
        str = str.replace('jQuery{}(','')
        return json.loads(str[str.find('{'):str.rfind('}') + 1])

def get_pin():
    """获取 PIN，用正则表达式从页面中取出"""
    url = "https://pcsitepp-fm.jd.com/"
    r = session.get(url)
    loginPin = re.findall('<input type="hidden" id="loginPin" value="(\w+)" />', r.text)
    pin = loginPin[0] if len(loginPin) > 0 else None
    return pin

def skuProResultPC(orderId, skuId, pin):
    """判断订单是否保价超时"""
    url = "https://sitepp-fm.jd.com/rest/webserver/skuProResultPC"
    data = {
        "orderId": orderId,
        "skuId": skuId,
        "pin": pin
    }
    headers = {
        'User-Agent': user_agent,
        'Referer': 'https://pcsitepp-fm.jd.com/',
    }

    r = session.post(url, data=data, headers=headers)
    return 'overTime' not in r.text

def get_order_list(pin, page_num=1):
    """保价列表"""

    # 存放订单信息
    order_info = []
    # 存放数量
    count_dir = {}

    url = "https://pcsitepp-fm.jd.com/rest/pricepro/priceskusPull"
    data = {"page": page_num, "pageSize": 10}
    headers = {
        'User-Agent': user_agent,
        'Referer': 'https://pcsitepp-fm.jd.com/',
    }
    r = session.post(url, headers= headers, data=data)

    # 订单之间的分隔符
    orders = r.text.split('<tr class="sep-row"><td colspan="6"></td></tr>')
    orders.pop(0)

    for item in orders:
        # 订单号
        orderid = re.findall("订单号：(\d+)", item)
        # 数量
        count_html = re.findall('<span class="count">([\sx\d]+)</span>',item)
        # 商品的 sku和序号
        skuidAndSequences = re.findall("queryOrderSkuPriceParam\.skuidAndSequence\.push\(\"(\d+\,\d+)\"\)\;", item)
        newSkuidAndSequences = []

        # 商品的sku和订单商品的序号
        for ss in skuidAndSequences:

            # 判断订单保价是否超时
            if skuProResultPC(orderid[0], ss.split(',')[0], pin):

                newSkuidAndSequences.append(ss)
                count_ss = count_html[int(ss.split(',')[1]) - 1]
                count = count_ss.replace('\t', '').replace('\n', '').replace('x', '')
                # 把 "订单号_sku" 当做 key
                count_dir[orderid[0] + '_' + ss.split(',')[0]] = count

        if newSkuidAndSequences:

            order_info.append({'orderid': orderid[0], 'skuidAndSequence': newSkuidAndSequences})

    if orders:
        """递归的方式获取所有的商品"""
        bill_info_sub, count_dir_sub = get_order_list(pin, page_num + 1)
        order_info.extend(bill_info_sub)
        count_dir.update(count_dir_sub)
    return order_info, count_dir

def get_price_list(pin):
    '''获取下单价格、商品信息、当前价格、数量'''

    product_list = []

    # 取订单号，sku和商品数量
    queryOrderPriceParam,count_dir = get_order_list(pin)

    # 获取购买时的价格
    params = {"queryOrderPriceParam": json.dumps(queryOrderPriceParam)}
    r = session.post("https://sitepp-fm.jd.com/rest/webserver/getOrderListSkuPrice", data = params)
    orderList = r.json()


    for item in orderList:

        skuid = item.get("skuid")
        buyingjdprice = item.get("buyingjdprice")
        orderid = item.get("orderid")

        # 商品信息
        product_info = get_product_info(skuid)
        # 当前价格
        price = get_product_price(product_info)
        # 优惠券
        coupon = get_product_coupon(product_info, price)

        name = product_info['name']
        count = count_dir[orderid + '_' + skuid]
        product_list.append({'orderid': orderid, 'name': name, 'price': price, 'coupon': coupon, 'count': count, 'buyingjdprice': buyingjdprice})
    return product_list

def protect_protect_apply(product_list):
    """申请价格保护"""

    if len(product_list) == 0:
        return
    else:
        for item in product_list:
            result = '订单号：{}，名称：{}, 数量：{}, 购买价格：{}, 当前价格：{}, 当前优惠：{}。'\
                .format(item['orderid'],
                        item['name'],
                        item['count'],
                        item['buyingjdprice'],
                        item['price'],
                        ' | '.join(item['coupon']))

            # 没有优惠券并且购买价格高于当前价格
            if len(item['coupon']) == 0 and item['buyingjdprice'] > item['price']:

                url = 'https://pcsitepp-fm.jd.com//rest/pricepro/skuProtectApply'
                data = {
                    "orderId": item['orderId'],
                    "orderCategory": "Others",
                    "skuId": item['skuId'],
                    "refundtype": 1
                }

                headers = {
                    'User-Agent': user_agent,
                    'Referer': 'https://pcsitepp-fm.jd.com/',
                    'accept': 'application/json, text/javascript, */*; q=0.01'
                }
                session.post(url, data=data, headers=headers)
                print(result + ' 已申请价格保护，请结果查看价格保护页面')

            elif len(item['coupon']) > 0:
                print(result + ' 在优惠券未申请自动价格保护，请联系客服申请')
    return




def get_product_price(project_info):

    url = "https://c0.3.cn/stock?skuId={}&area={}&venderId={}&buyNum=1&choseSuitSkuIds=&cat={}&extraParam={{%22originid%22:%221%22}}&fqsp=0&ch=1&callback=jQuery{}"\
        .format(project_info['skuId'],
                project_info['area'],
                project_info['venderId'],
                project_info.get('cat', ''),
                random.randint(1000000, 9999999))
    headers = {
        'User-Agent': user_agent,
        'Host': 'c0.3.cn',
        'Referer':  'https://item.jd.com/{0}.html'.format(project_info['skuId']),
    }
    r = session.get(url, headers=headers)
    data = parse_json(r.text)
    # 价格
    price = data.get("stock", {}).get("jdPrice", {}).get('p', 0)
    return float(price)

def get_product_info(skuId):
    """获商品信息"""
    info = {}
    url = "http://item.jd.com/%s.html" % skuId
    headers = {
        'User-Agent': user_agent,
        'Referer': 'https://pcsitepp-fm.jd.com/',
    }
    r = requests.get(url, headers=headers)
    pageConfig = re.findall("var pageConfig = \{([\s\S]+)\} catch\(e\) \{\}", r.text)
    cat = re.findall("cat: \[([\d,]+)\]", pageConfig[0])
    venderId = re.findall("venderId:(\d+)", pageConfig[0])
    shopId = re.findall("shopId:'(\d+)'", pageConfig[0])
    name = re.findall("name: '(.+)'", pageConfig[0])
    info['cat'] = cat[0] if len(cat) else ""
    info['venderId'] = venderId[0] if len(venderId) else ""
    info['shopId'] = shopId[0] if len(shopId) else ""
    info['skuId'] = skuId
    # 配送区域默认为北京
    info['area'] = '1_72_55653_0'
    info['name'] = name[0]
    return info

def get_product_coupon(product_info, price):
    """优惠券列表"""
    result = []
    headers = {
        'User-Agent': user_agent,
        'Referer':  'https://item.jd.com/{0}.html'.format(product_info['skuId']),
    }
    url = 'https://cd.jd.com/promotion/v2?callback=jQuery{}&skuId={}&area={}&shopId={}&venderId={}&cat={}&isCanUseDQ=1&isCanUseJQ=1&platform=0&orgType=2&jdPrice={}&appid=1&_={}'\
        .format(
                str(random.randint(1000000, 9999999)),
                product_info['skuId'],
                product_info['area'],
                product_info['shopId'],
                product_info['venderId'],
                product_info['cat'].replace(',', '%2C'),
                price,
                str(int(time.time() * 1000)))
    r = session.get(url, headers=headers)
    data = parse_json(r.text)
    pickOneTag = data.get("prom", {}).get("pickOneTag")

    # 满减
    if pickOneTag:
        for tag in pickOneTag:
            result.append(tag.get('content'))

    # 打折
    skuCoupon = data.get('skuCoupon')
    if skuCoupon:
        for coupon in skuCoupon:
            if coupon.get('allDesc'):
                result.append(coupon.get('allDesc'))
            elif coupon.get('quota') and coupon.get('discount'):
                result.append("满" + str(coupon.get('quota')) + '减' + str(coupon.get('discount')))
    return result

if __name__ == '__main__':
    show_QRcode()
    time.sleep(10)
    ticket = check_QRcode()
    validation_QRcode(ticket)
    pin = get_pin()
    product_list = get_price_list(pin)
    protect_protect_apply(product_list)
    print("完成了")

