
import requests
from bs4 import BeautifulSoup
import time

userAgent = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
        }

def parse_html(event, context):
    now = time.time()
    authorIds = ['1222805984']
    for author in authorIds:
        url = 'https://zhiyou.smzdm.com/member/' + author + '/baoliao/'


        html_content = requests.get(url, headers = userAgent).content

        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
        infos = soup.find_all(name='div',attrs={'class': 'pandect-content-stuff'})


        for info in infos:
            a = info.find(name='div', attrs={'class': 'pandect-content-title'}).a
            t = info.find(name='span', attrs={'class': 'pandect-content-time'}).text

            # 只推送 5分钟之内的爆料
            content_time = time.mktime(time.strptime('2021-' + t + ':00', "%Y-%m-%d %H:%M:%S"))
            if((now - content_time) < 5 * 60):
                content = a.text.strip() + '\r\n' + a['href']
                push_qmsg(content)


def push_qmsg(msg):
    key = 'xxx'
    url = 'https://qmsg.zendee.cn/send/' + key
    msg = {'msg':  msg}
    requests.post(url, params=msg)
