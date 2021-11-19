
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import etree
import requests
import re
import threading
import os



def crawler_front_page():
    headers = {
        'Referer': 'http://fund.eastmoney.com/data/fundranking.html',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Cookie': 'qgqp_b_id=c7106e55b1ba3768660d7e8411ea4759; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; st_si=59746599501191; st_asi=delete; ASP.NET_SessionId=1gwfj4cqojpf5ktiylgmy43o; EMFUND0=null; EMFUND8=11-17%2019%3A05%3A47@%23%24%u94F6%u6CB3%u6587%u4F53%u5A31%u4E50%u6DF7%u5408@%23%24005585; EMFUND9=11-18 11:03:50@#$%u524D%u6D77%u5F00%u6E90%u65B0%u7ECF%u6D4E%u6DF7%u5408A@%23%24000689; st_pvi=17535190085817; st_sp=2021-09-27%2017%3A30%3A48; st_inirUrl=https%3A%2F%2Fnews.google.com%2F; st_sn=9; st_psi=20211118112357985-112200312936-9119693474'
    }

    response = requests.get('http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=6yzf&st=desc&sd=2020-11-18&ed=2021-11-18&qdii=&tabSubtype=,,,,,&pi=1&pn=10000&dx=1&v=0.6791917206798068', headers=headers)

    response.encoding = 'utf-8'
    return response.text

def parse_front_page(html):

    return re.findall(r"\d{6}",html)

def get_stock_url(codes):
    
    url = []
    for code in codes:
        url.append("http://fundf10.eastmoney.com/ccmx_{}.html".format(code))
        
    return url

def is_element(driver, type, element_name):
    try:
        WebDriverWait(driver,2).until(EC.presence_of_element_located((type ,element_name)))
        return True
    except:
        return False
    
def crawler_stock_page(c,stock_url_list):
    count = c.split(",") 
    driver = webdriver.Chrome('D:\personal\gitpython\chromedriver.exe')
    file = "D:/fund/fund_{}.txt".format(count[0])

    
    for url in stock_url_list[int(count[0]):int(count[1])]:
        stock_result = []
        title = "没有数据"

        try:
            driver.get(url)

            element_result = is_element(driver, By.CLASS_NAME, "tol")
            if element_result:
                wait = WebDriverWait(driver, 3)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tol')))
                
                if is_element(driver, By.XPATH, '//*[@id="cctable"]/div[1]/div/div[3]/font/a'):
                    driver.find_element_by_xpath('//*[@id="cctable"]/div[1]/div/div[3]/font/a').click()
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tol')))
            
                stock_xpath = etree.HTML(driver.page_source )
                stock_result = stock_xpath.xpath("//div[@id='cctable']//div[@class='box'][1]//td[3]//text()")
                title = stock_xpath.xpath('//*[@id="cctable"]/div[1]/div/h4/label[1]/a')[0].text

            with open(file, 'a+') as f:
                    f.write("{'name': '" + title + "', 'stock': ['"+'\',\''.join(stock_result) + "']}\n")    
        except:
            continue

    

def thread_test(*args):
    threads = []
    for crawler_count in ["0,3"]:
        t = threading.Thread(target=crawler_stock_page, args=(crawler_count, args[0]))   
        threads.append(t)

    for t in threads:
        t.start()      
    for t in threads:
        t.join()         

def parse_data():
    result = {}
    stock = {}

    files= os.listdir('D:/fund/')

    for file in files:
        for line in open('D:/fund/' + file):
            data = eval(line.strip())
            key = data['name']
            if key == '没有数据' or key in result:
                continue
                
            result[key] = data['stock']

            for value in data['stock']:
                if value in stock:
                    stock[value] = stock[value] + 1
                else:
                    stock[value] = 1
        
        with open('D:/fund_result/stock.csv', 'a+') as f:
            for key in stock:
                f.write(key + "," + str(stock[key]) + "\n") 
        
        with open('D:/fund_result/fund.csv', 'a+') as f:   
            for key in result:
                values = []
                for value in result[key]:
                    values.append('{}({})'.format(value, stock[value]))
                f.write(key + ',' + ','.join(values) + '\n')
    

 
if __name__ == '__main__':
    html = crawler_front_page()
    codes = parse_front_page(html)
    url_list = get_stock_url(codes)
    thread_test(url_list)
    # parse_data()
