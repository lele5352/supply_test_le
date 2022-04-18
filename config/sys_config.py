from config import env_configs

#测试环境配置
env = 'test_160' #160环境
# env = 'test_uat' #160环境
#env = 'test_26' #26环境

env_config = env_configs.get(env)

user = {
    'username': 'huanglele@popicorns.com',
    'password': '123456'
}

url = "http://10.0.0.127:8192/#/task/mylist",  # 160发版机