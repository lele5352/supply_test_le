from robots.wms_robot import WmsAppRobot, WmsServiceRobot
from config import env_config, db_config
from tools.mysql_operator import MySqlOperator

wms = WmsAppRobot()
# pda = PdaController()
wms_service = WmsServiceRobot("transfer")


# mysql_info = db_config
# mysql_report = MySqlOperator(mysql_info, 'supply_report')