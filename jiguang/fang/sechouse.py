import random
import requests
from bs4 import BeautifulSoup
import re
import math
from lxml import etree

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
chinese_city_district_dict = dict()
chinese_area_dict = dict() 

def create_headers():
    headers = dict()
    headers["User-Agent"] = random.choice(USER_AGENTS)
    headers["Referer"] = "http://www.ke.com"
    return headers

class SecHouse(object):
    def __init__(self, district, area, name, price, desc, pic):
        self.district = district
        self.area = area
        self.price = price
        self.name = name
        self.desc = desc
        self.pic = pic
    
    def text(self):
        return self.district + "," + \
                self.area + "," + \
                self.name + "," + \
                self.price + "," + \
                self.desc + "," + \
                self.pic

def get_districts():
    url = 'https://bj.ke.com/xiaoqu/'
    headers = create_headers()
    response = requests.get(url, timeout=10, headers=headers)
    html = response.content
    root = etree.HTML(html)
    elements = root.xpath('///div[3]/div[1]/dl[2]/dd/div/div/a')
    en_names = list()
    ch_names = list()
    for element in elements:
        link = element.attrib['href']
        en_names.append(link.split('/')[-2])
        ch_names.append(element.text)

    # 打印区县英文和中文名列表
    for index, name in enumerate(en_names):
        chinese_city_district_dict[name] = ch_names[index]
    return en_names

def get_areas(district):
    page = "http://bj.ke.com/xiaoqu/{0}".format(district)
    areas = list()
    try:
        headers = create_headers()
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        root = etree.HTML(html)
        links = root.xpath('//div[3]/div[1]/dl[2]/dd/div/div[2]/a')

        # 针对a标签的list进行处理
        for link in links:
            relative_link = link.attrib['href']
            # 去掉最后的"/"
            relative_link = relative_link[:-1]
            # 获取最后一节
            area = relative_link.split("/")[-1]
            # 去掉区县名,防止重复
            if area != district:
                chinese_area = link.text
                chinese_area_dict[area] = chinese_area
                # print(chinese_area)
                areas.append(area)
        return areas
    except Exception as e:
        print(e)

with open("sechouse.txt", "w", encoding='utf-8') as f:
    # 开始获得需要的板块数据
    total_page = 1
    sec_house_list = list()
    districts = get_districts()
    for district in districts:
        arealist = get_areas(district)
        for area in arealist:
            # 中文区县
            chinese_district = chinese_city_district_dict.get(district, "")
            # 中文版块
            chinese_area = chinese_area_dict.get(area, "")
            page = 'http://bj.ke.com/ershoufang/{0}/'.format(area)
            print(page)
            headers = create_headers()
            response = requests.get(page, timeout=10, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            # 获得总的页数
            try:
                page_box = soup.find_all('div', class_='page-box')[0]
                matches = re.search('.*data-total-count="(\d+)".*', str(page_box))
                total_page = int(math.ceil(int(matches.group(1)) / 10))
            except Exception as e:
                print(e)

            print(total_page)
            # 从第一页开始,一直遍历到最后一页
            headers = create_headers()
            for i in range(1, total_page + 1):
                page = 'http://bj.ke.com/ershoufang/{0}/pg{1}'.format(area,i)
                print(page)
                response = requests.get(page, timeout=10, headers=headers)
                html = response.content
                soup = BeautifulSoup(html, "lxml")

                # 获得有小区信息的panel
                house_elements = soup.find_all('li', class_="clear")
                for house_elem in house_elements:
                    price = house_elem.find('div', class_="totalPrice")
                    name = house_elem.find('div', class_='title')
                    desc = house_elem.find('div', class_="houseInfo")
                    pic = house_elem.find('a', class_="img").find('img', class_="lj-lazy")

                    # 继续清理数据
                    price = price.text.strip()
                    name = name.text.replace("\n", "")
                    desc = desc.text.replace("\n", "").strip()
                    pic = pic.get('data-original').strip()

                    # 作为对象保存
                    sec_house = SecHouse(chinese_district, chinese_area, name, price, desc, pic)
                    print(sec_house.text())
                    sec_house_list.append(sec_house)
                    
            for sec_house in sec_house_list:
                f.write(sec_house.text() + "\n")

