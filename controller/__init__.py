from controller.ums_controller import UmsController
from config.sys_config import env_config


ums = UmsController()
headers = ums.ums_login()

web_prefix = env_config.get("web_prefix")
app_prefix = env_config.get("app_prefix")
transfer_service_prefix = env_config.get('transfer_service_prefix')