from PIL import ImageGrab
import requests
import base64
from urllib.parse import quote_plus


def tuling(text):
    """
    图灵机器人
    :return:
    """

    host = 'http://openapi.tuling123.com/openapi/api/v2'
    data = {
        "reqType":0,              # 输入类型:0-文本(默认)、1-图片、2-音频
        "perception": {           # 输入信息
            "inputText": {        # 文本信息
                "text": text
            }
        },
        "userInfo": {              # 用户信息
            "apiKey": "8d78a28535c947e69c2ddbcc5efeed51",
            "userId": "1234567"
        }
    }
    response = requests.post(host, json=data)
    if response:
        return response.json()['results'][0]['values']['text']
    else:
        return '错误了！'

def fetch_token():
    """
    获取语音合成 token
    :return: token
    """

    access_token = ""

    api_key = 'Pd4uoyvt1cwD7n2sHtLd5Ov0'
    secret_key = '8BnaPRcv3tTNa94eaFVfFy1pW2UkmvrO'

    token_url = 'http://openapi.baidu.com/oauth/2.0/token'
    params = {'grant_type': 'client_credentials',
              'client_id': api_key,
              'client_secret': secret_key}
    response = requests.post(token_url, params)
    if response:
        access_token = response.json()['access_token']
    return access_token


def synthesized_speech(text, token):
    """
    合成语音
    """

    mp3_path = "/Users/xx/Desktop/siri/result.mp3"

    tts_url = 'http://tsn.baidu.com/text2audio'

    tex = quote_plus(text)  # 此处TEXT需要两次urlencode
    # tok:token，tex：文本，per：发音人，spd：语速（0-15）默认 5，pit：音调（0-15）默认 5，
    # vol：音量（0-9）默认 5，aue：下载的文件格式, 3 mp3(default)、4 pcm-16k、5 pcm-8k、6 wav，
    # cuid：用户唯一标识，lan ctp 固定参数
    params = {'tok': token, 'tex': tex, 'per': 4, 'spd': 5, 'pit': 5, 'vol': 5, 'aue': 3, 'cuid': "pythonjishu", 'lan': 'zh', 'ctp': 1}

    response = requests.post(tts_url, params)
    if response:
        with open(mp3_path, 'wb') as of:
            of.write(response.content)


def grab_img():
    """
    截图
    :return:
    """

    img_path = "/Users/xx/Desktop/siri/grab.png"
    # bbbox 的参数为截取屏幕的一部分，距离左边像素，上边像素，右边像素，下边像素

    img = ImageGrab.grab(bbox=(2630,80,3330,1290))
    img.save(img_path)
    return img_path

def fench_ocr_token():
    """
    获取ocr token
    :return: token
    """

    api_key = 'ioE84jDQmGNLG7heN6rovF9Q'
    secret_key = 'qGVyAobVtCGKdD1Ncz60IvGMdf3dP1ct'

    access_token = ""
    url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+api_key+'&client_secret='+secret_key
    response = requests.get(url)
    if response:
        access_token = response.json()['access_token']
    return access_token

def ocr(img_path, access_token):
    """
    通用文字识别
    :return: 识别后的文字
    """

    text = ""
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        words_result = response.json()['words_result']
        print(words_result)
        text = words_result[-1]['words']
    return text


if __name__ == '__main__':
    token = fetch_token()
    ocr_token = fench_ocr_token()
    siri_speak_text = "嗨，机器人！"
    while 1:
        text = tuling(siri_speak_text)
        synthesized_speech(text, token)
        img_path = grab_img()
        siri_speak_text = ocr(img_path, ocr_token)


