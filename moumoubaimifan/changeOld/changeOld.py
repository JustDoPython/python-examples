import json
import base64
import time
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.iai.v20200303 import iai_client
from tencentcloud.iai.v20200303 import models as models03

from tencentcloud.ft.v20200304 import ft_client,models


sid = "xx"
skey = "xx"
try: 

    filepath = '/Users/imeng/Downloads/face/face.png'
    file = open(filepath, "rb")
    
    base64_data = base64.b64encode(file.read())

    cred = credential.Credential(sid, skey) 
    httpProfile = HttpProfile()
    httpProfile.endpoint = "iai.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = iai_client.IaiClient(cred, "ap-beijing", clientProfile) 

    req = models03.DetectFaceAttributesRequest()
    params = {
        "MaxFaceNum":2,
        "Action":"DetectFace",
        "Version":"2018-03-01",
        "Image": base64_data.decode()
    }
    req.from_json_string(json.dumps(params))

    resp = client.DetectFaceAttributes(req) 
    faceDetailInfos = resp.FaceDetailInfos
    
    httpProfile.endpoint = "ft.tencentcloudapi.com"
    clientProfile.httpProfile = httpProfile
    client = ft_client.FtClient(cred, "ap-beijing", clientProfile) 

    req = models.ChangeAgePicRequest()

    for age in range(70, 80):
        params = {
            "Image": base64_data.decode(),
            "AgeInfos": [
                {
                    "Age": age,
                    "FaceRect": {
                        "Y": faceDetailInfos[0].FaceRect.Y,
                        "X": faceDetailInfos[0].FaceRect.X,
                        "Width": faceDetailInfos[0].FaceRect.Width,
                        "Height": faceDetailInfos[0].FaceRect.Height
                    } 
                },
                {
                    "Age": age,
                    "FaceRect": {
                        "Y": faceDetailInfos[1].FaceRect.Y,
                        "X": faceDetailInfos[1].FaceRect.X,
                        "Width": faceDetailInfos[1].FaceRect.Width,
                        "Height": faceDetailInfos[1].FaceRect.Height
                    } 
                }
            ],
            "RspImgType": "base64"
        }
        req.from_json_string(json.dumps(params))
        resp = client.ChangeAgePic(req) 
        image_base64 = resp.ResultImage
        image_data = base64.b64decode(image_base64)
        file_path = '/Users/imeng/Downloads/face/{}.png'.format(age)
        with open(file_path, 'wb') as f:
            f.write(image_data)
        time.sleep(1)
except TencentCloudSDKException as err: 
    print(err) 
