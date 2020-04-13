# 识别多个车牌
from aip import AipOcr

APP_ID = '自己的 App ID'
API_KEY = '自己的 Api Key'
SECRET_KEY = '自己的 Secret Key'
# 创建客户端对象
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
# 建立连接的超时时间，单位为毫秒
client.setConnectionTimeoutInMillis(5000)
# 通过打开的连接传输数据的超时时间，单位为毫秒
client.setSocketTimeoutInMillis(5000)

# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content('cars.png')
options = {}
# 参数 multi_detect 默认为 false
options['multi_detect'] = 'true'
res = client.licensePlate(image, options)
for wr in res['words_result']:
    print('车牌号码：' + wr['number'])
    print('车牌颜色：' + wr['color'])