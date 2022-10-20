from tools.request_operator import RequestOperator
from tools.mysql_operator import MySqlOperator
from controller import *
from config.api_config.wms_service import wms_service_config
from tools.log_operator import logger as log
import time

class WmsServiceController(RequestOperator):

    def __init__(self):
        self.prefix = transfer_service_prefix
        self.headers = headers
        super().__init__(self.prefix, self.headers)

        # self.db = MySqlOperator(**env_config.get("mysql_info_ims"))


    def service_demand_create(self, **kwargs):
        """
            新增调拨需求
            :param kwargs:
            :return: res.data
        """
        wms_service_config.get("transferDemand_create")["data"].update(kwargs)
        res = self.send_request(**wms_service_config.get("transferDemand_create"))
        if res.get("code") == 200:
            log.info(res)
            print("新增调拨需求：", res)
            return res
        else:
            log.error(res)
            return

    def service_demand_cancel(self, **kwargs):
        """
            取消调拨需求
            :param kwargs:
            :return:
        """
        wms_service_config.get("transferDemand_cancel")["data"].update(kwargs)
        res = self.send_request(**wms_service_config.get("transferDemand_cancel"))
        if res.get("code") == 200:
            log.info(res)
            print("取消调拨需求：", res)
            return res.get("data")
        else:
            log.error(res)
            return

if __name__ == '__main__':
    wms_service = WmsServiceController()
    kw = {"demandType": 2, "goodsSkuCode": "BP53586714577C01", "bomVersion": "C"}
    res = wms_service.service_demand_create(**kw)
    demand_code = res.get("data")["demandCode"]

    kw = {"demandCode": demand_code}
    res = wms_service.service_demand_cancel(**kw)
    print(res)