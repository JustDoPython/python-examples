import requests

send_data = {
   "question": '你的梦想是什么？',      #构建发送的数据
   "api_key": "a6ec389908bcc23fceb2bbe998e3313e",
   "api_secret": "bsa0yv06pl1p"
}
api_url = 'http://i.itpk.cn/api.php'
chat_content = requests.post(api_url, data=send_data)    #发送请求数据
print(chat_content.text)