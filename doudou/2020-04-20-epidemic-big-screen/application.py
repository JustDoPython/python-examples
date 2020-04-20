from flask import Flask, render_template
import datetime
import json
import redis
import pandas as pd

app = Flask(__name__)

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)


@app.route('/')
def index():
    return render_template('a.html')


@app.route('/global')
def global_index():
    context = {
        'date': get_date(),
        'statistics_data': json.loads(r.get('foreign_data')),
        'country_data': get_rank_data(),
        'article_data': json.loads(r.get('article_data'))
    }
    return render_template('global.html', **context)


@app.route('/china')
def china_index():
    china_data = get_china_data()
    context = {
        'date': get_date(),
        'statistics_data': china_data[0],
        'country_data': china_data[1],
        'article_data': json.loads(r.get('article_data'))
    }
    return render_template('china.html', **context)


def get_date():
    today = datetime.date.today()
    yesterday = today + datetime.timedelta(days=-1)
    return {'today': today.strftime('%Y.%m.%d'), 'yesterday': yesterday.strftime('%m月%d日')}


# 国外详细数据
def get_rank_data():
    df = pd.DataFrame(json.loads(r.get('rank_data')), columns=['name', 'confirmAdd', 'confirm', 'heal', 'dead'])
    return df.sort_values('confirm', ascending=False).values.tolist()


# 国内详细数据
def get_china_data():
    china_data = json.loads(r.get('china_data'))
    statistics_data = {'nowConfirmAdd': china_data['chinaAdd']['confirm'],
                       'healAdd': china_data['chinaAdd']['heal'],
                       'deadAdd': china_data['chinaAdd']['dead'],
                       'nowConfirm': china_data['chinaTotal']['nowConfirm'],
                       'confirm': china_data['chinaTotal']['confirm'],
                       'heal': china_data['chinaTotal']['heal'],
                       'dead': china_data['chinaTotal']['dead'],
                       }

    df = pd.DataFrame(china_data['province'],
                      columns=['name', 'import_abroad', 'now_confirm', 'confirm', 'heal', 'dead'])
    province_list = df.sort_values('now_confirm', ascending=False).values.tolist()

    return statistics_data, province_list


@app.route('/global_top10')
def get_global_top10():
    df = pd.DataFrame(json.loads(r.get('rank_data')), columns=['name', 'confirmAdd', 'confirm', 'heal', 'dead'])
    top10 = df.sort_values('confirmAdd', ascending=True).tail(10)
    result = {'country': top10['name'].values.tolist(), 'data': top10['confirmAdd'].values.tolist()}
    return json.dumps(result)


@app.route('/global_map')
def get_global_map():
    df = pd.DataFrame(json.loads(r.get('rank_data')), columns=['name', 'confirmAdd', 'confirm', 'heal', 'dead'])
    records = df.to_dict(orient="records")
    china_data = json.loads(r.get('china_data'))
    result = {
        'confirmAdd': [{'name': '中国', 'value': china_data['chinaAdd']['confirm']}],
        'confirm': [{'name': '中国', 'value': china_data['chinaTotal']['confirm']}],
        'heal': [{'name': '中国', 'value': china_data['chinaTotal']['heal']}],
        'dead': [{'name': '中国', 'value': china_data['chinaTotal']['dead']}]
    }

    for item in records:
        result['confirmAdd'].append({'name': item['name'], 'value': item['confirmAdd']})
        result['confirm'].append({'name': item['name'], 'value': item['confirm']})
        result['heal'].append({'name': item['name'], 'value': item['heal']})
        result['dead'].append({'name': item['name'], 'value': item['dead']})

    return json.dumps(result)


@app.route('/china_top10')
def get_china_top10():
    china_data = json.loads(r.get('china_data'))
    df = pd.DataFrame(china_data['province'],
                      columns=['name', 'import_abroad', 'now_confirm', 'confirm', 'heal', 'dead'])
    top10 = df.sort_values('import_abroad', ascending=True).tail(10)
    result = {'country': top10['name'].values.tolist(), 'data': top10['import_abroad'].values.tolist()}
    return json.dumps(result)


@app.route('/china_map')
def get_china_map():
    china_data = json.loads(r.get('china_data'))
    df = pd.DataFrame(china_data['province'], columns=['name', 'import_abroad', 'now_confirm', 'confirm', 'heal', 'dead'])
    records = df.to_dict(orient="records")
    result = {
        'now_confirm': [],
        'confirm': [],
        'heal': [],
        'dead': []
    }

    for item in records:
        result['now_confirm'].append({'name': item['name'], 'value': item['now_confirm']})
        result['confirm'].append({'name': item['name'], 'value': item['confirm']})
        result['heal'].append({'name': item['name'], 'value': item['heal']})
        result['dead'].append({'name': item['name'], 'value': item['dead']})

    return json.dumps(result)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5200, debug=True)
    # print(get_china_data()[1])
