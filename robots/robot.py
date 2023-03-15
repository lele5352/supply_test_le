from tools.log_operator import logger as log
import requests
import time
import json


class Robot(object):

    def __init__(self, prefix=None, headers=None):
        self.headers = headers
        self.prefix = prefix

    def call_api(self, uri_path, method, data):
        url = self.prefix + uri_path
        log.info('请求内容：%s' % json.dumps({'method': method, 'url': url, 'data': data}, ensure_ascii=False))
        log.info('请求头：%s' % json.dumps(self.headers, ensure_ascii=False))

        if method == 'get':
            res = requests.get(url, headers=self.headers, params=data)
        elif method == 'post':
            res = requests.post(url, headers=self.headers, json=data)
        elif method == 'put':
            res = requests.put(url, headers=self.headers, json=data)
        res_data = res.json()
        return res_data