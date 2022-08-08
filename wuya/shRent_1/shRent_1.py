#通过某租房网站首页接口爬取租房房源信息
import time, re, csv, requests
import codecs
from bs4 import BeautifulSoup

list=['jingan','xuhui','huangpu','changning','putuo','pudong','baoshan','hongkou','yangpu','minhang','jinshan','jiading','chongming','fengxian','songjiang','qingpu']
print("****处理开始****")
with open(r'..\document\sh.csv', 'wb+')as fp:
    fp.write(codecs.BOM_UTF8)
f = open(r'..\document\sh.csv','w+',newline='', encoding='utf-8')
writer = csv.writer(f)
urls = []

for a in list:
    urls.append('https://sh.lianjia.com/zufang/{}/pg1rco11/'.format(a))
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36'}

    res = requests.get('https://sh.lianjia.com/zufang/{}/pg1rco11/'.format(a), headers=headers)
    content = res.text
    soup = BeautifulSoup(content, 'html.parser')
    page_num = int(soup.find('div', attrs={'class': 'content__pg'}).attrs['data-totalpage'])
    for i in range(2,page_num+1):
        urls.append('https://sh.lianjia.com/zufang/{}/pg{}rco11/'.format(a,i))

print(urls)

num=1
for url in urls:
    print("正在处理第{}页数据...".format(str(num)))
    res1 = requests.get(url, headers=headers)
    content1 = res1.text
    soup1 = BeautifulSoup(content1, 'html.parser')
    infos = soup1.find('div', {'class': 'content__list'}).find_all('div', {'class': 'content__list--item'})

    for info in infos:

        house_url = 'https://sh.lianjia.com' + info.a['href']
        title = info.find('p', {'class': 'content__list--item--title'}).find('a').get_text().strip()
        group = title.split()[0][3:]
        price = info.find('span', {'class': 'content__list--item-price'}).get_text()
        tag = info.find('p', {'class': 'content__list--item--bottom oneline'}).get_text()
        mixed = info.find('p', {'class': 'content__list--item--des'}).get_text()
        mix = re.split(r'/', mixed)
        address = mix[0].strip()
        area = mix[1].strip()
        door_orientation = mix[2].strip()
        style = mix[-1].strip()
        region = re.split(r'-', address)[0]
        writer.writerow((house_url, title, group, price, area, address, door_orientation, style, tag, region))
        time.sleep(0)
    print("第{}页数据处理完毕，共{}条数据。".format(str(num), len(infos)))
    num+=1


f.close()
print("****全部完成****")

