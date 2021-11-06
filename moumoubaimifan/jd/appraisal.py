# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import json

headers = {
    'cookie': '自己 cookie',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
}

def all_appraisal():
    appraisal = {}
    url = "https://club.jd.com/myJdcomments/myJdcomment.action?sort=0"
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    url = soup.find('ul', class_='tab-trigger');
    for li in url.find_all('li'):
        contents = li.a.text
        b = li.b
        if b != None:
            appraisal[contents] = int(b.text)
    return appraisal


def be_evaluated(appraisal):
     for i in range((appraisal['待评价订单'] // 20) + 1):
        url = 'https://club.jd.com/myJdcomments/myJdcomment.action?sort=0&page={}'.format(i + 1)
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, "html.parser")
        table = soup.find('table', class_ = 'td-void order-tb');
        tbodys = table.find_all('tbody')
        for order in tbodys:
            oid = order.find('span', class_="number").a.text
            product = order.find('div', class_='p-name').a
            pname = product.text
            pid=product['href'].replace('//item.jd.com/', '').replace('.html', '')
            content = pname + '，东西质量非常好，与卖家描述的完全一致，非常满意,真的很喜欢，完全超出期望值，发货速度非常快，包装非常仔细、严实，物流公司服务态度很好，运送速度很快，很满意的一次购物'
            

            saveProductComment_url = "https://club.jd.com/myJdcomments/saveProductComment.action"
            saveProductComment_data = {
                'orderId': oid,
                'productId': pid,  
                'score': '5',
                'content': bytes(content, encoding="gbk"),  
                'saveStatus': '1',
                'anonymousFlag': '1'
            }
            save = requests.post(saveProductComment_url, headers=headers, data=saveProductComment_data)
            time.sleep(5)

def be_shown_img():
    url = 'https://club.jd.com/myJdcomments/myJdcomment.action?sort=1'
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    pro_info = soup.find_all('div', class_ = 'pro-info');
    for plist in pro_info:
        oid = plist['oid']
        pid = plist['pid']
        
        img_url = 'https://club.jd.com/discussion/getProductPageImageCommentList.action?productId={}'.format(pid)
        img_req = requests.get(img_url, headers=headers)
        text = img_req.text
        print(img_url)

        result = json.loads(text)
        imgurl = result["imgComments"]["imgList"][0]["imageUrl"]
        

        saveUrl = 'https://club.jd.com/myJdcomments/saveShowOrder.action'
        img_data = {
            'orderId': oid,
            'productId': pid,
            'imgs': imgurl,
            'saveStatus': 3
        }
        print(img_data)
        header = headers
        header['Referer'] = 'https://club.jd.com/myJdcomments/myJdcomment.action?sort=1'
        header['Origin'] = 'https://club.jd.com'
        header['Content-Type'] = 'application/x-www-form-urlencoded'
        requests.post(saveUrl, data=img_data, headers=header)
        time.sleep(5)

def review():

    appraisal = all_appraisal() 
    saveUrl = 'https://club.jd.com/afterComments/saveAfterCommentAndShowOrder.action'
    for i in range((appraisal['待评价订单'] // 20) + 1):

        url = 'https://club.jd.com/myJdcomments/myJdcomment.action?sort=3&page={}'.format(i+1)
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, "html.parser")
        operates = soup.find_all('div', class_='operate')
        for o in operates:
            href = o.a['href']
            infos = href.replace('http://club.jd.com/afterComments/productPublish.action?sku=','').split('&orderId=');
            pid = infos[0]
            oid = infos[1]

            data = {
                'orderId': oid,
                'productId': pid,
                'content': bytes('宝贝和想象中差不多所以好评啦，对比了很多家才选择了这款，还是不错的，很NICE！真的', encoding='gbk'),
                'imgs': '', 
                'anonymousFlag': 1,
                'score': 5
            }

            requests.post(saveUrl, headers=headers, data=data)

            time.sleep(5)

def service_rating():
    appraisal = all_appraisal() 
    saveUrl = 'https://club.jd.com/myJdcomments/insertRestSurvey.action?voteid=145&ruleid={}'
    for i in range((appraisal['服务评价'] // 20) + 1):
        url = "https://club.jd.com/myJdcomments/myJdcomment.action?sort=4&page={}".format(i + 1)
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, "html.parser")
        trs = soup.find_all('tr', class_='tr-th');
        for tr in trs:
            oid = tr.find('span', class_='number').a.text
            saveUrl = saveUrl.format(oid)
            data = {
                'oid': oid,
                'gid': 69,
                'sid': 549656,
                'stid': 0,
                'tags': '',
                'ro1827': '1827A1',
                'ro1828': '1828A1',
                'ro1829': '1829A1',
            }
            requests.post(saveUrl, headers=headers, data=data)
            print('订单号：' + oid + '服务评价完成')
            time.sleep(5)

if __name__ == '__main__':
    # appraisal = all_appraisal() 
    service_rating()
    
