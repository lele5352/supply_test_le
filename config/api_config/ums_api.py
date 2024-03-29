from config.api_config import ApiConfig
ums_api_config = {
    "get_public_key": {
        "uri_path": "/api/ec-ums-api/user/rsa/publicKey",
        "method": "GET",
        "data": {'t': 0}
    },
    "login": {
        "uri_path": "/api/ec-ums-api/user/login",
        "method": "post",
        "data": {
            "code": "dw2m",
            "grant_type": "password",
            "password": '123456',
            "randomStr": "",
            "scope": "server",
            "username": 'huanglele@popicorns.com',
        }
    },
    "user_search": {
        "uri_path": "/api/ec-ums-api/user/page",
        "method": "get",
        "data": {
            "current": 1,
            "size": 15,
            "total": 100,
            "username": "",
            "nickname": "",
            "delFlag": 0
        }
    }
}


class UmsApi:
    class GetPublicKey(ApiConfig):
        uri_path = "/api/ec-ums-api/user/rsa/publicKey"
        method = "GET"
        data = {'t': 0}

    class Login(ApiConfig):
        uri_path = "/api/ec-ums-api/user/login"
        method = "POST"
        data = {
            "code": "dw2m",
            "grant_type": "password",
            "password": '123456',
            "randomStr": "",
            "scope": "server",
            "username": 'huanglele@popicorns.com',
        }

    class UserSearch(ApiConfig):
        uri_path = "/api/ec-ums-api/user/page"
        method = "GET"
        data = {
            "current": 1,
            "size": 15,
            "total": 100,
            "username": "",
            "nickname": "",
            "delFlag": 0
        }