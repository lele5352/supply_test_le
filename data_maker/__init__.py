from controller.wms_controller import WmsController
from controller.stockoperation_controller import StockOpearationController
from controller.oms_controller import OmsController
from controller.pda_controller import PdaController
from controller.wms_service_controller import WmsServiceController
from config import env_config

#最新
from robots.wms_robot import WmsServiceRobot


web_prefix = env_config.get("web_prefix")
app_prefix = env_config.get("app_prefix")
transfer_service_prefix = env_config.get('transfer_service_prefix')


wms = WmsController()
st = StockOpearationController()
oms = OmsController()
pda = PdaController()
# wms_service = WmsServiceController()   不适用

wms_service_robot = WmsServiceRobot("transfer")


mysql_info = env_config.get('mysql_info')
# mysql_report = MySqlOperator(mysql_info, 'supply_report')