from controller.ums_controller import UmsController
from config import env_config
from robots import app_headers


web_prefix = env_config.get("app")
app_prefix = env_config.get("app")
transfer_service_prefix = env_config.get("transfer")
