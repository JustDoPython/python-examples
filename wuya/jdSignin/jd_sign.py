#pt_key=AAJi2BVXADDKWR6SHbo_ARE3SS6Bv7y-nKo0aWKLQjiYCcmreYfTUHN15o-nlRdh2M3iwV5kYv8; pt_pin=zhongulou; 
import requests

pt_key="替换为自己的pt_key"
pt_pin="替换为自己的pt_pin"
cookie="pt_key={}; pt_pin={}".format(pt_key, pt_pin)
url = "https://api.m.jd.com/client.action?functionId=signBeanAct&body=%7B%22fp%22%3A%22-1%22%2C%22shshshfp%22%3A%22-1%22%2C%22shshshfpa%22%3A%22-1%22%2C%22referUrl%22%3A%22-1%22%2C%22userAgent%22%3A%22-1%22%2C%22jda%22%3A%22-1%22%2C%22rnVersion%22%3A%223.9%22%7D&appid=ld";
headers = {
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "okhttp/3.12.1;jdmall;android;version/10.3.4;build/92451;",
    "Cookie": cookie
}

response = requests.post(url=url, headers=headers)
print(response.text)

res = response.json()
returnMes = ""

if(res.get("errorMessage")==None):
    returnMes = "签到成功！"
else:
    returnMes = "签到失败".format(res.get("errorMessage"))

requests.get("https://sctapi.ftqq.com/这里填写你个人的SendKey.send?title={}".format(returnMes))