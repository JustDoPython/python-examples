"""
右侧：最新动态
https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoNewsArticleList

左侧：地区柱状图：新增 确诊 死亡
https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist


中间上方：国内：现有确诊 确诊 治愈 死亡 境外输入 无症状感染者 国外：现有确诊 确诊 治愈 死亡
# 国内数据 https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5
# 国外数据 https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalStatis


中间下方：地图：确诊、治愈、死亡
# 国内数据：https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5
# 国外数据：https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist

"""

import requests
import json
import redis

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)


def pull_data_from_web(url):
    response = requests.get(url, headers=header)
    return json.loads(response.text) if response.status_code == 200 else None


# 获取最新动态数据
def get_article_data():
    data = pull_data_from_web('https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoNewsArticleList')
    if data is None:
        return ''
    return [[item['publish_time'], item['url'], item['title']] for item in data['data']['FAutoNewsArticleList']]


# 获取各个国家当前【新增、确诊、治愈、死亡】数据
def get_rank_data():
    data = pull_data_from_web('https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist')
    if data is None:
        return ''
    return [[item['name'], item['confirmAdd'], item['confirm'], item['heal'], item['dead']] for item in data['data']]


# 获取国内统计数据【现有确诊 确诊 治愈 死亡 境外输入 无症状感染者】 & 各省份详细数据（确诊、治愈、死亡）
def get_china_data():
    data = pull_data_from_web('https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5')
    if data is None:
        return ''
    dict = json.loads(data['data'])
    province_res = []
    for province in dict['areaTree'][0]['children']:
        name = province['name']
        now_confirm = province['total']['nowConfirm']
        confirm = province['total']['confirm']
        heal = province['total']['heal']
        dead = province['total']['dead']
        import_abroad = 0
        for item in province['children']:
            if item['name'] == '境外输入':
                import_abroad = item['total']['confirm']
                break
        province_res.append([name, import_abroad, now_confirm, confirm, heal, dead])
    return {'chinaTotal': dict['chinaTotal'], 'chinaAdd': dict['chinaAdd'], 'province': province_res}


# 获取国外统计数据【现有确诊 确诊 治愈 死亡】
def get_foreign_data():
    data = pull_data_from_web('https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalStatis')
    if data is None:
        return ''
    return data['data']['FAutoGlobalStatis']


article_data = get_article_data()
r.set('article_data', json.dumps(article_data))

rank_data = get_rank_data()
r.set('rank_data', json.dumps(rank_data))

china_data = get_china_data()
r.set('china_data', json.dumps(china_data))

foreign_data = get_foreign_data()
r.set('foreign_data', json.dumps(foreign_data))
