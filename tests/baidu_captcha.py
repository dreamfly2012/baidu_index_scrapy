# encoding: utf-8
import time
import urllib, base64
from urllib import parse
import requests

import json
import base64
import re


def get_token(API_Key, Secret_Key):
    # 获取access_token
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + API_Key + '&client_secret=' + Secret_Key
    r = requests.get(host)
    content_json = r.json()
    access_token = content_json['access_token']
    return access_token


def recognition_word_high(filepath, filename, access_token):
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=' + access_token
    # 二进制方式打开图文件
    data = open(filepath + filename, 'rb').read()
    b64data = base64.b64encode(data)
    files = {'image': b64data}
    data = parse.urlencode(files).encode('utf-8')
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(url, data=data, headers=headers)
    content = bytes.decode(r.content)
    json_content = json.loads(content)
    if (r.ok):
        if ('error_code' in json_content):
            print(json_content['error_msg'])
        else:
            for each in json_content['words_result']:
                print(each['words'])


if __name__ == '__main__':
    API_Key = "kqMf8CDL62pOeP2pIy2MZc40"
    Secret_Key = "NxCeFtTG9joPdBr87Bk3oIo758Yhm763"
    filepath = "./"
    filename = "a.bmp"
    access_token = get_token(API_Key, Secret_Key)
    recognition_word_high(filepath, filename, access_token)
