import requests
import json
from config.api_config.ums_api import ums_api_config

class RequestOperator:
    def __init__(self, prefix, headers):
        self.prefix = prefix
        self.headers = headers

    def send_request(self, uri_path, method, data):
        print(self.prefix, type(uri_path), method, data)
        url = self.prefix + uri_path
        data = data
        res = requests.get(url,headers=self.headers, data=json.dumps(data))
        res_data = res.json()
        return res_data



if __name__ == '__main__':
    pass