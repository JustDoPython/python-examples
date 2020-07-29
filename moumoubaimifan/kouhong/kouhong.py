import base64

import requests
from PIL import Image, ImageDraw


ak = 'MbDXGOrgXHqsgHKlAZLv6K93'

sk = 'fzIOiK2aEAKntAY7cOEHkUCoZOawe0wR'

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+ak+'&client_secret=' + sk
response = requests.get(host)
if response:
    access_token = response.json()['access_token']
    print(access_token)
else:
    raise Exception('access_token 获取失败')



# 图片转 base64
pic_path = '/Users/xx/Desktop/kh/原图.png'
with open (pic_path, 'rb') as f:
    base64_data = base64.b64encode(f.read())

# image：图片，image_type：图片格式，face_field：请求的结果，landmark150为人脸的 150 个关键点
params = '{"image":"'+base64_data.decode('utf-8')+'","image_type":"BASE64","face_field":"landmark150"}'
request_url = 'https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token=' + access_token
headers = {'content-type': 'application/json'}
response = requests.post(request_url, data=params, headers=headers)

if response:
    face = response.json()
else:
    raise Exception('人脸关键点获取失败')


# 上嘴唇关键点，按顺时针方向的顺序组成一个多边形
mouth_lip_upper_point_list = [
    'mouth_corner_right_outer','mouth_lip_upper_outer_1','mouth_lip_upper_outer_2','mouth_lip_upper_outer_3',
    'mouth_lip_upper_outer_4','mouth_lip_upper_outer_5','mouth_lip_upper_outer_6','mouth_lip_upper_outer_7',
    'mouth_lip_upper_outer_8','mouth_lip_upper_outer_9','mouth_lip_upper_outer_10','mouth_lip_upper_outer_11',
    'mouth_corner_left_outer','mouth_corner_left_inner','mouth_lip_upper_inner_11','mouth_lip_upper_inner_10',
    'mouth_lip_upper_inner_9','mouth_lip_upper_inner_8','mouth_lip_upper_inner_7','mouth_lip_upper_inner_6',
    'mouth_lip_upper_inner_5','mouth_lip_upper_inner_4','mouth_lip_upper_inner_3','mouth_lip_upper_inner_2',
    'mouth_lip_upper_inner_1','mouth_corner_right_inner','mouth_corner_right_outer'
]

# 下嘴唇关键点，按顺时针方向的顺序组成一个多边形
mouth_lip_low_point_list = [
    'mouth_corner_right_outer','mouth_corner_right_inner','mouth_lip_lower_inner_1','mouth_lip_lower_inner_2',
    'mouth_lip_lower_inner_3','mouth_lip_lower_inner_4','mouth_lip_lower_inner_5','mouth_lip_lower_inner_6',
    'mouth_lip_lower_inner_7','mouth_lip_lower_inner_8','mouth_lip_lower_inner_9','mouth_lip_lower_inner_10',
    'mouth_lip_lower_inner_11','mouth_corner_left_outer','mouth_lip_lower_outer_11','mouth_lip_lower_outer_10',
    'mouth_lip_lower_outer_9','mouth_lip_lower_outer_8','mouth_lip_lower_outer_7','mouth_lip_lower_outer_6',
    'mouth_lip_lower_outer_5','mouth_lip_lower_outer_4','mouth_lip_lower_outer_3','mouth_lip_lower_outer_2',
    'mouth_lip_lower_outer_1','mouth_corner_right_outer'
]


# 将将转为可操作的 RGBA 模式
img = Image.open(pic_path)
d = ImageDraw.Draw(img, 'RGBA')

for f in face['result']['face_list']:
    # 上嘴唇关键点 [(x,y),(x,y),(x,y)] 元组列表
    mouth_lip_upper_list = []
    # 下嘴唇关键点 [(x,y),(x,y),(x,y)] 元组列表
    mouth_lip_low_list = []

    for point in mouth_lip_upper_point_list:
        p = f['landmark150'][point]
        mouth_lip_upper_list.append((p['x'], p['y']))

    for point in mouth_lip_low_point_list:
        p = f['landmark150'][point]
        mouth_lip_low_list.append((p['x'], p['y']))



    # 口红颜色
    hex = input('请输入口红的16进制颜色：')
    color = (int(hex[1:3], 16), int(hex[3:5], 16), int(hex[5:7], 16))

    # 绘制多边形并填充颜色
    d.polygon(mouth_lip_upper_list, fill=color)
    # 绘制边框并填充颜色
    d.line(mouth_lip_upper_list, fill=color, width = 1)

    d.polygon(mouth_lip_low_list, fill=color)
    d.line(mouth_lip_low_list, fill=color, width=1)

img.show()
img.save('/Users/xx/Desktop/kh/' + hex + '.png')



