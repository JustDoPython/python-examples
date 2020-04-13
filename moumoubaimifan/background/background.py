from PIL import Image
import requests
import base64


def get_access_token():
    """
    获取 access_token
    """
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=ak&client_secret=sk'
    response = requests.get(host)
    if response:
        return response.json()['access_token']


def get_foreground(originalImagePath):
    """
    人像分割
    """
    # 二进制方式打开图片文件
    f = open(originalImagePath, 'rb')
    img = base64.b64encode(f.read())

    # 请求 百度 AI 开放平台
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_seg?access_token=" + get_access_token()
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    params = {"image": img}
    response = requests.post(request_url, data=params, headers=headers)

    if response:
        foreground = response.json()['foreground']
        img_data = base64.b64decode(foreground)
        img_path = 'foreground.png'
        with open(img_path, 'wb') as f:
            f.write(img_data)
        return Image.open(img_path)


def get_background():
    """
    背景图片
    """
    color = ('red', 'blue', 'white')
    imgs = []
    for c in color:
        # 一寸照片大小
        img = Image.new("RGBA", (295, 413), c)
        imgs.append(img)
    return imgs

def mian():
    fore = get_foreground('original.jpg')
    p = fore.resize((330, 415))
    r,g,b,a = p.split()

    imgs = get_background()
    for img in imgs:
        img.paste(p, (-30, 50), mask=a)
        img.show()

if __name__ == '__main__':
    mian()