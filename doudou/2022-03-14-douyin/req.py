# coding:utf-8

import requests as req
import time

import urllib3

urllib3.disable_warnings()


def send_get(url, params, cookie):
    time.sleep(5)
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13D15 MicroMessenger/7.0.9(0x17000929) NetType/WIFI Language/zh_CN",
        "cookie": cookie
    }
    # response = req.get(url, headers=headers,  verify=False)
    response = req.get(url, headers=headers, params=params, verify=False)
    return response.text


def send_post(url, params, cookie):
    time.sleep(2)
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13D15 MicroMessenger/7.0.9(0x17000929) NetType/WIFI Language/zh_CN",
        "cookie": cookie
    }
    response = req.post(url, headers=headers, data=params, verify=False)
    return response.text
