from config.evn_config import *

# new
env = 'test160' #160环境
# env = 'test189' #189环境
# env = 'uat' #uat环境
#env = 'test26' #26环境

env_config = prefix_config.get(env)
db_config = mysql_config.get(env)

user = {
    'username': 'huanglele@popicorns.com',
    'password': '123456'
}
