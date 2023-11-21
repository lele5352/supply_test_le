import requests
from locust import HttpUser, TaskSet, task
import os
from random import randint

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class TestReturnOrderNoGenerate(TaskSet):
    def on_start(self):
        self.headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1SWQiOjEsInVzZXJfbmFtZSI6ImFkbWluIiwidiI6NDIsInNjb3BlIjpbImFsbCJdLCJleHAiOjE2Mjc1ODA4MzIsImp0aSI6IjA4ZmMzMWViLTk1NWUtNGEwYS05NzMyLTY0NTdlYjFkMjk0YyIsImNsaWVudF9pZCI6ImhvbWFyeS1lYyJ9.mFximYw7Na8ZHWr2wR58dOy6vFPC6oALkDNLpETKYsGjv1OtEqmRn7dZ-N2AyTmO8PSqgOlXHnH0gceaVOtrP_sxH1otfWkTgBRQfXsKZ48uW_uXLmiZgfrWqHYsFZH-kHUUfQQaexzauzmLCGkNzby-DN30lhGcVd0LnZycBx4'
        }
        self.data = {'aaa': '1', 'bbb': 'a'}
        self.generate_datas()

        # self.ranIndex = randint(0, len(self.data) - 1)

    def generate_datas(self):
        self.data_list = []
        for i in range(0, 5):
            self.data.update({'aaa': i})
            self.data_list.append(self.data)

    @task(1)
    def test_return_order_generate(self):
        self.data_list.pop()

        # print(self.data_list[self.ranIndex])
        # 定义请求参数
        print(self.data)
        """
        with self.client.post('api/ec-wms-api/entryorder', headers=self.headers, json=data,
                              catch_response=True) as response:
            result = response.json()
            print(result)
            if result['code'] == 200:
                response.success()
            else:
                response.failure('Failed!')
        """

class WebSitUser(HttpUser):
    tasks = [TestReturnOrderNoGenerate]
    min_wait = 1000  # 单位为毫秒
    max_wait = 1000  # 单位为毫秒


if __name__ == "__main__":
    os.system("locust -f locust_ams_add.py --host=https://test-160.popicorns.com/")
