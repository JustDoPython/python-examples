import httpx
import base64

def getAccessToken():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    clientId = '2r...Yq' # 换成你的
    clientSecret = 'd6...Dd' # 换成你的
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (clientId, clientSecret)
    response = httpx.get(host)
    if response.status_code == 200:
        ret = response.json()
        return ret.get('access_token')
    else:
        raise "获取AccessToken失败:" + str(response.status_code)

def imageRecognition(image):
    img = base64.b64encode(image)
    params = {"image":img}
    access_token = getAccessToken()
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = httpx.post(request_url, data=params, headers=headers)
    if response.status_code == 200:
        return response.json().get("result")
    else:
        raise "获取AccessToken失败:" + str(response.status_code)

if __name__ == "__main__":
    # print(getAccessToken())
    imagefilepath = r'C:\Users\alisx\Pictures\road.jpg'
    with open(imagefilepath,"rb") as f:
        print(imageRecognition(f.read()))
