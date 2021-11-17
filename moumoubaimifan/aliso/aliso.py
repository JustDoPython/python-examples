# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import string


word = input('请输入要搜索的资源名称：')
    
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}

result_list = []
for i in range(1, 11):
    print('正在搜索第 {} 页'.format(i))
    params = {
        'page': i,
        'keyword': word,
        'search_folder_or_file': 0,
        'is_search_folder_content': 0,
        'is_search_path_title': 0,
        'category': 'all',
        'file_extension': 'all',
        'search_model': 2
    }
    response_html = requests.get('https://www.alipanso.com/search.html', headers = headers,params=params)
    response_data = response_html.content.decode()
   
    soup = BeautifulSoup(response_data, "html.parser");
    divs = soup.find_all('div', class_='resource-item border-dashed-eee')
    
    if len(divs) <= 0:
        break

    for div in divs[1:]:
        p = div.find('p',class_='em')
        if p == None:
            break

        download_url = 'https://www.alipanso.com/' + div.a['href']
        date = p.text.strip();
        name = div.a.text.strip();
        result_list.append({'date':date, 'name':name, 'url':download_url})
    
    if len(result_list) == 0:
        break
    
result_list.sort(key=lambda k: k.get('date'),reverse=True)
print(result_list)

with open("aliso.html", encoding='utf-8') as t:
    template = string.Template(t.read())

final_output = template.substitute(elements=result_list)
with open("report.html", "w", encoding='utf-8') as output:
    output.write(final_output)
