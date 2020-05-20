import requests

send_data = {
   "key": "9fd874929409453991db78f8b46a446b",
   "info": '我叫你一声你敢答应吗',      #构建发送的数据
   "userid": "622952"
}
api_url = 'http://www.tuling123.com/openapi/api'
chat_content = requests.post(api_url, data=send_data)    #发送请求数据
print(chat_content.text)