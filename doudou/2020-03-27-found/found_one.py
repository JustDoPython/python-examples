import requests

startDate = '2012-05-04'
endDate = '2020-03-01'
foundCode = '510300'
pageSize = 3000
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Referer': f'http://fundf10.eastmoney.com/jjjz_{foundCode}.html'
}

url = f'http://api.fund.eastmoney.com/f10/lsjz?&fundCode={foundCode}&pageIndex=1&pageSize={pageSize}&startDate={startDate}&endDate={endDate}&_=1585302987423'
response = requests.get(url, headers=header)


def write_file(content):
    filename = f'found_{foundCode}.txt'
    with open(filename, 'a') as f:
        f.write(content + '\n')


write_file(response.text)
