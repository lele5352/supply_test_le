import requests
import time
import json
from tools.log_operator import logger as log
from config.api_config.ums_api import ums_api_config


class RequestOperator:
    def __init__(self, prefix,  headers):
        self.prefix = prefix
        self.headers = headers
        self.time_tamp = int(time.time() * 1000)

    def send_request(self, uri_path, method, data):
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



if __name__ == '__main__':
    pass