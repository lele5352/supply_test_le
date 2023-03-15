import time
from tools.log_operator import logger as log

from tools.request_operator import RequestOperator
from tools.rsq_operator import encrypt_data
# from config.api_config.ums_api import ums_api_config
from config.api_config.ums_api import UmsApi
# from config.sys_config import env_config, user
from config import env_config, user


class UmsController(RequestOperator):
    def __init__(self):
        self.prefix = env_config.get('app')
        self.headers = {'Content-Type': 'application/json;charset=UTF-8', "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
        super().__init__(self.prefix, self.headers)

    def get_public_key(self):
        timestamp = int(time.time() * 1000)
        UmsApi.GetPublicKey.data.update({'t': timestamp})
        info = UmsApi.GetPublicKey.get_attributes()
        res = self.send_request(**info)
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
        UmsApi.Login.data.update({
            "password": user['password'],
            "username": user['username']
        })

        try:
            info = UmsApi.Login.get_attributes()
            res = self.send_request(**info)
            authorization_str = res['data']['tokenHead'] + ' ' + res['data']['token']
            headers = {'Content-Type': 'application/json;charset=UTF-8', "Authorization": authorization_str,
                       "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
            print(headers)
            return headers
        except Exception as e:
            print('账号登录失败！', e)
            return None

    def get_app_headers(self):
        return self.ums_login()

    def user_search(self):
        self.headers = self.get_app_headers()
        info = UmsApi.UserSearch.get_attributes()
        res = self.send_request(**info)
        print(res)


