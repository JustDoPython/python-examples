import requests,re

url = 'https://mp.weixin.qq.com/s/C6P5RwIejmUrnovom3lZFg'

result = requests.get(url).text
biz = re.search(r'__biz=(.*?)&amp;',result)[1]
mid = re.search(r'mid=(.*?)&amp;',result)[1]
vid = re.search(r'wxv_(.*?)\"',result)[0].replace('\"', '')

video_url = f'https://mp.weixin.qq.com/mp/videoplayer?action=get_mp_video_play_url&preview=0&__biz={biz}&mid={mid}&idx=1&vid={vid}&uin=&key=&pass_ticket=&wxtoken=777&devicetype=&clientversion=&__biz={biz}&appmsg_token=&x5=0&f=json'

url_info = requests.get(video_url).json()['url_info'][0]['url']

resp = requests.get(url_info, stream=True )

with open('day10.mp4', 'wb') as f:
    f.write(resp.content)

print('视频下载完成')
