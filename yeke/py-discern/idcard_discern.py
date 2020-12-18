from aip import AipOcr

APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
# 创建客户端对象
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
# 打开并读取文件内容
fp = open("card.jpg", "rb").read()
# res = client.basicGeneral(fp) # 普通
res = client.basicAccurate(fp) # 高精度
# 遍历结果
for tex in res["words_result"]:
    row = tex["words"]
    print(row)