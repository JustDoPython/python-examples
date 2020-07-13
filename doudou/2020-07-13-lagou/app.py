import requests
import time


def headers_to_dict(headers):
    headers = headers.split("\n")
    d_headers = dict()
    for h in headers:
        if h:
            k, v = h.split(":", 1)
            if k == 'cookie' and d_headers.get(k, None) is not None:
                d_headers[k] = d_headers.get(k) + "; " + v.strip()
            else:
                d_headers[k] = v.strip()
    return d_headers


home_url = 'https://www.lagou.com/jobs/list_python?px=new&city=%E5%85%A8%E5%9B%BD'
url = 'https://www.lagou.com/jobs/positionAjax.json?px=new&needAddtionalResult=false'
headers = """
accept: application/json, text/javascript, */*; q=0.01
origin: https://www.lagou.com
referer: https://www.lagou.com/jobs/list_python?px=new&city=%E5%85%A8%E5%9B%BD
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36
"""

headers_dict = headers_to_dict(headers)


def get_data_from_cloud(page):
    params = {
        'first': 'false',
        'pn': page,
        'kd': 'python'
    }
    s = requests.Session()  # 创建一个session对象
    s.get(home_url, headers=headers_dict, timeout=3)  # 用session对象发出get请求，请求首页获取cookies
    cookie = s.cookies  # 为此次获取的cookies
    response = requests.post(url, data=params, headers=headers_dict, cookies=cookie, timeout=3)
    result = response.text
    write_file(result)


def write_file(content):
    filename = 'data.txt'
    with open(filename, 'a') as f:
        f.write(content + '\n')


"""
工作地点地图 ： city
行业分布：industryField
学历要求：education
工作经验：workYear
薪资：salary
所需技能：skillLables
福利：companyLabelList
类型：firstType、secondType
"""
def get_data():
    for i in range(76):
        page = i + 1
        get_data_from_cloud(page)
        time.sleep(5)


get_data()