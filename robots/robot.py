from tools.log_operator import logger as log
from config import env_config
from robots import app_prefix, app_headers, service_headers
import requests
import time
import json


class Robot(object):

    def __init__(self, prefix=None, headers=None):
        self.prefix = prefix
        self.headers = headers

    def call_api(self, uri_path, method, data=None, files=None):
        url = self.prefix + uri_path
        if method == "GET":
            res = requests.get(url, params=data, headers=self.headers)
        elif method == "POST":
            res = requests.post(url, json=data, headers=self.headers, files=files)
        elif method == "PUT":
            res = requests.put(url, json=data, headers=self.headers)
        elif method == "DELETE":
            res = requests.delete(url, headers=self.headers)
        else:
            raise ValueError("Invalid request method")

        log.info("请求头：%s" % json.dumps(self.headers, ensure_ascii=False))
        log.info("请求内容：%s" % json.dumps({"method": method, "url": url, "data": data}, ensure_ascii=False))
        log.info(f"traceId：{res.headers.get('Trace-Id')}")
        log.info("响应内容：" + json.dumps(res.json(), ensure_ascii=False))
        log.info(
            "-------------------------------------------------我是分隔符-------------------------------------------------")
        return res.json()

    @staticmethod
    def time_tamp():
        return int(time.time() * 1000)

    def respond_result(self, name, respond):

        if respond:
            if respond.get("code") == 200:
                log.info(respond)
                print("{0}: {1}".format(name, respond.get("message")))
                return respond.get("data")
            else:
                log.error(respond)
                return
        else:
            return None


class AppRobot(Robot):

    def __init__(self):
        super().__init__(app_prefix, app_headers)


class ServiceRobot(Robot):

    def __init__(self, service_name):
        self.prefix = env_config.get(service_name)
        super().__init__(self.prefix, service_headers)

