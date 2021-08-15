import requests
import json

def get_check_data(date, limit=1, sessionid='4551f206c64'):
    headers = {
        'authority': 'bushu.jingdaka.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': 'beegosessionID=%s;' % sessionid,
    }

    params = (
        ('team_id', '0'),
        ('search_name', ''),
        ('course_id', '1099357'),
        ('record_at', date),
        ('calendar_id', '0'),
        ('limit', limit),
        ('offset', '0'),
    )

    response = requests.get('https://bushu.jingdaka.com/bg/course/userdatedata', headers=headers, params=params)
    data = json.loads(response.text)
    rows = []
    if data['err_code'] == 0:
        for d in data['data']['user_data']:
            if d['user_id'] not in [53433468,53433325]:
                rows.append((d['user_id'], date, '√'))
    else:
        print("抓取出错了:", data)
    return rows

if __name__ == '__main__':
    print(get_check_data('2021-08-04'))