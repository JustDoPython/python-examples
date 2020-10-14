import requests
import csv
import time
from requests import RequestException
from bs4 import BeautifulSoup


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'referer': 'https://piao.qunar.com/',
    'cookie': 'QN1=0000048030682631e2b8e754; QN99=9790; QN300=s%3Dbing; _i=DFiEZnlDE06wWY2e-VJVB_sesBww; fid=7bffafe6-c57b-4fe2-a347-57564cf0e66f; QunarGlobal=10.86.213.148_-ba9ffe3_173d2293375_-522b|1596959542130; QN601=6087af8bc791a83b1722cf1f3a337261; QN48=000018002f10273189b0bd0e; QN621=1490067914133%3DDEFAULT%26fr%3Dqunarindex; QN668=51%2C55%2C59%2C56%2C59%2C55%2C59%2C55%2C55%2C57%2C57%2C52%2C52; quinn=449c5a2ddd5098e4f741c730191aa6912eabaf034aa8231814cd7f5efb7ca1dbcff43ae3475ce1d71b90ad243bc206c6; SC1=21fa2e00edea939d117d9a7e41129b1c; SC18=; QN205=s%3Dbing; QN277=s%3Dbing; csrfToken=HomfccFgWNTkPHmFVLrLHhlXCV6mjpsX; QN269=A21E61200CA111EBA025FA163E26B699; QN163=0; QN71="MTE3LjEzNi4xMi4xOTA65bm/5LicOjE="; QN57=16025173972310.18425984059497624; QN243=22; Hm_lvt_15577700f8ecddb1a927813c81166ade=1602517398,1602517783; QN63=%E7%83%AD%E9%97%A8%E6%99%AF%E7%82%B9; _vi=g_OFZoprSNiT8bT2fhMMgWQhy-acGZ71z08p4vqpe6lVRC2Xv29cXK1WQEMpCBGx_4IHmo0unplzjb6oGmuoAhUZNNr22jOvzOiFBCsn4Q7AbvU8itcY097o-NJQC3d9gVplwq7h5uOrek1Kr7dV3MmHblSRGp_fqwibyoi9LuUx; QN267=016328531675c329458; QN58=1602521369113%7C1602521608108%7C2; JSESSIONID=21D7E279F1794E089E322E748FFE3B89; Hm_lpvt_15577700f8ecddb1a927813c81166ade=1602521609; QN271=a6ad6f7e-c46f-453f-aa1a-110855ad9ec7; __qt=v1%7CVTJGc2RHVmtYMS9CR1htaXZ6S0tkcVg3c3AyaGI0TnN4VmIwR1BXeldqYWJFZXlnekV0VnpJNjRCK2VrS1Axek8vb0dLZ25JM1F1WE83SURKU2dOd3lPb1I0UHVoSzNZWG43MnFRdTh0alJXTGdpK1BETUVNYTk0ejQ2cmpPNXNRazAwNUpsYXViNENwV0ovY09TYnIzcHgwc3AvYkpLUk4reXZkdTVHMXJVPQ%3D%3D%7C1602521615121%7CVTJGc2RHVmtYMS9DMHJaQlpialhNRXJKcXo1SkNBSzdKZXFxQmRWV01QbnFUSEdEMXNNZzBsZjI3U0ZNTWxjei9PeFBkcDNKUlp3MWxnb29SbjNPemc9PQ%3D%3D%7CVTJGc2RHVmtYMSt5UmRsK1BMMDJUZHRMSDlhR1lMNXhPbXNIeVMyNk9DdGgraTJ6OXJHbEdQWXhrZCtmN1hDeDhlRGlMQThLRDJOK1hTV2VYd1EvaDdVcmZnNDNaYTE0cnE2bklsNENIcjlYRVNTdExxb01BNy9ZQlFwTFE5VHp3dTJHRjI5SE1mTCtIRXMvb25FSXVxbEY5UTdPcVlYSzZlU1phK1pDVmhOZElsL1BlNmtROXVGMmhJb1FKd3hxV3F3Qyt5OTc5K3Zjdk9zVjhsMzN3VEN2ZUN3WGx6VGJ2OFYwYSsvMDBWYmpLNFhMRk8xQWd1WmxsNzU5TXRKV2lTdDFZbEZpaUlMV1ZSQkZOSk50dVRqVDh4WFRSQ0lqUUdXd2U2eXBydVBDaXhSWDRWUklHV3hGRDVLQkwyQ2J4emlvaU5tZzNIbENFb2g0YWFndGhDZnFvV3dpaEJMYkpNNWQzdDkvTzF5S1FPVWJpTlhvRFFZcDFXSnJzMWRUZUNvT1MrSU4zVHJiRER4MkdZRWMxMEtCKzBXai9RanVoMzNyWUt0Qi9CbFZLOXViYlo5eXBVaXZwTzMyMWtrSGRnaGNydy9BVzIyWEFoRjBKN1QwTEtwdVE5QWJqa1BLa0kzWUJDWGVOZVdMWjdVQjRnb1ppSXdHM3VFZWxsZDlRZUI0SUtBeXRSVjAyT0Znck8xdUsxY2taVzQyMzk0UUJUZ20wQjRJRk5VbUdhN2VPR0Q3STl1YTlOdnNSV2d2TVk5K1kzRjh3bzVXbHZ3eFdxQnBVeER3YW5JOTVOd0RXZnVQd0xqWmVMSFNSNStCaFVkNGJ5WGdBRHRabUJacktpbnVwV2MzWDIvTmwxaDdpK1l1VElYRGJreTdSUURWOEtaTFlwT3dwNktPQ3pUalJuNFBxYVEyanZFb2V4aGRyVFJ4Mmw3UEg4aDk5Y1gzZklPdlJnRGE3SVJGMnRydkMvMkIzVVFmZUp6NXFteUxZZXFSa2FveDA5dE1GaTVOWjZPVWZ4emZZRmFnQW1OQ0NiQ0ROempjZzBaMTdXSDZqM2YrVlVBNGJDZz0%3D'
}

excel_file = open('data.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(excel_file)
writer.writerow(['名称', '城市', '类型', '级别', '热度', '地址'])


def get_page_html(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_content(content, subject, url):
    if not content:
        print('content is none ', url)
        return;
    soup = BeautifulSoup(content, "html.parser")
    search_list = soup.find(id='search-list')
    items = search_list.find_all('div', class_="sight_item")
    for item in items:
        name = item['data-sight-name']
        districts = item['data-districts']
        address = item['data-address']
        level = item.find('span', class_='level')
        level = level.text if level else ''
        star = item.find('span', class_='product_star_level')
        star = star.text if star else ''
        writer.writerow([name, districts, subject, level, star, address])
    # print(name, districts, address, id, level, star)


subjects = ['文化古迹', '自然风光', '农家度假', '游乐场', '展馆', '古建筑', '城市观光']


def get_data():
    for subject in subjects:
        for page in range(10):
            page = page + 1
            url = F'https://piao.qunar.com/ticket/list.htm?keyword=热门景点&region=&from=mps_search_suggest&subject={subject}&page={page}&sku='
            print(url)
            content = get_page_html(url)
            parse_content(content, subject, url)
            time.sleep(5)


if __name__ == '__main__':
    get_data()
