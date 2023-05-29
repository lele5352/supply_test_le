from config.api_config.ums_api import UmsApi
from tools.rsq_operator import encrypt_data
from config import env_config, user
from urllib.parse import urljoin
import time
import requests
import json


app_prefix = env_config.get("app")
transfer_service_prefix = env_config.get("transfer")


def login():
    """
     登录完拼装出来的鉴权字符串
    :return: headers
    """
    # 先获取公钥
    key_count = UmsApi.GetPublicKey.get_attributes()
    login_content = UmsApi.Login.get_attributes()

    timestamp = int(time.time() * 1000)
    UmsApi.GetPublicKey.data.update({'t': timestamp})
    url = urljoin(app_prefix, key_count['uri_path'])
    res = requests.get(url, params=key_count['data']).json()

    # 获取到公钥之后拼装begin和end返回
    key = res['data']
    begin = '-----BEGIN PUBLIC KEY-----\n'
    end = '\n-----END PUBLIC KEY-----'
    try:
        public_key = begin + key + end
        # 加密密码并更新密码为加密后的

        encrypt_password = encrypt_data(user['password'], public_key)
        user['password'] = encrypt_password
        data = login_content['data']
        data.update(
            {
                "password": user['password'],
                "username": user['username']
            }
        )
        url = urljoin(app_prefix, login_content['uri_path'])
        login_res = requests.post(url, json=data).json()
        authorization_str = login_res['data']['tokenHead'] + ' ' + login_res['data']['token']
        headers = {'Content-Type': 'application/json;charset=UTF-8', "Authorization": authorization_str}
        return headers
    except Exception as e:
        print('账号登录失败！', e)
        return None


def get_service_headers():
    username = user['username']
    # user_id = UMSDBOperator.query_sys_user(username).get('id')
    user_id = 308
    service_header = {"user": json.dumps({'username': username, 'user_id': user_id}), "serviceName": "ec-scm-service"}
    return service_header


app_headers = login()
service_headers = get_service_headers()


if __name__ == '__main__':
    login()
