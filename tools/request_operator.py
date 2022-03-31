import requests
import time
import json
from config.api_config.ums_api import ums_api_config


class RequestOperator:
    def __init__(self, prefix, headers):
        self.prefix = prefix
        self.headers = headers
        self.time_tamp = int(time.time()) * 1000

    def send_request(self, uri_path, method, data):
        url = self.prefix + uri_path
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