import time

from tools.request_operator import RequestOperator
from tools.rsq_operator import encrypt_data
from config.api_config.ums_api import ums_api_config
from config.sys_config import env_config, user

class UmsController(RequestOperator):
    def __init__(self):
        self.prefix = env_config.get('web_prefix')
        self.headers = {'Content-Type': 'application/json;charset=UTF-8', "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
        self.header = self.ums_login()
        super().__init__(self.prefix, self.headers)

    def get_public_key(self):
        timestamp = int(time.time() * 1000)
        ums_api_config['get_public_key']['data'].update({
            't': timestamp
        })
        res = self.send_request(**ums_api_config['get_public_key'])
        # 获取到公钥之后拼装begin和end返回
        key = res['data']
        begin = '-----BEGIN PUBLIC KEY-----\n'
        end = '\n-----END PUBLIC KEY-----'
        try:
            public_key = begin + key + end
            return public_key
        except TypeError:
            return

    def ums_login(self, specific_user=False, username='', password=''):
        """
        :param username: 用户名，仅指定用户账号时填写
        :param password: 密码，仅指定用户账号时填写
        :param specific_user: 是否指定用户登录
        :return: authorization_str: 登录完拼装出来的鉴权字符串
        """
        # 先获取公钥
        public_key = self.get_public_key()
        if not public_key:
            return

        # 如果指定账号登录，则用传的账密更新从配置中读取到的账密;否则读取配置中的默认用户的账密
        if specific_user:
            user.update(
                {
                    "username": username,
                    "password": password
                }
            )

        # 加密密码并更新密码为加密后的
        encrypt_password = encrypt_data(user['password'], public_key)
        user['password'] = encrypt_password
        ums_api_config['login']['data'].update(
            {
                "password": user['password'],
                "username": user['username']
            }
        )

        try:
            res = self.send_request(**ums_api_config['login'])
            authorization_str = res['data']['tokenHead'] + ' ' + res['data']['token']
            headers = {'Content-Type': 'application/json;charset=UTF-8', "Authorization": authorization_str,
                       "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
            return headers
        except:
            print('账号登录失败！')
            return None

    # def get_app_headers(self):
    #     authorization = self.ums_login()
    #     headers = {'Content-Type': 'application/json;charset=UTF-8', "Authorization": authorization, "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
    #     return headers

    def user_search(self):
        self.headers = self.get_app_headers()
        res = self.send_request(**ums_api_config['user_search'])
        print(res)




if __name__ == '__main__':
    UmsController().user_search()