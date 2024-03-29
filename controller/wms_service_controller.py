from tools.request_operator import RequestOperator
from tools.mysql_operator import MySqlOperator
from controller import *
from config.api_config.wms_api_config import TransferApiConfig
from tools.log_operator import logger as log
import time


class WmsServiceController(RequestOperator):

    def __init__(self):
        self.prefix = transfer_service_prefix
        self.headers = app_headers
        super().__init__(self.prefix, self.headers)

        # self.db = MySqlOperator(**env_config.get("mysql_info_ims"))


    def service_demand_create(self, **kwargs):
        """
            新增调拨需求
            :param kwargs:
            :return: res.data
        """
        TransferApiConfig.TransferDemandCreate.data.update(**kwargs)
        info = TransferApiConfig.TransferDemandCreate.get_attributes()
        res = self.send_request(**info)

        if res.get("code") == 200:
            log.info(res)
            print("新增调拨需求：", res["data"]["demandCode"])
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
        # wms_service_config.get("transferDemand_cancel")["data"].update(kwargs)
        TransferApiConfig.TransferDemandCancle.data.update(**kwargs)
        # res = self.send_request(**wms_service_config.get("transferDemand_cancel"))
        info = TransferApiConfig.TransferDemandCancle.get_attributes()
        res = self.send_request(**info)
        if res.get("code") == 200:
            log.info(res)
            print("取消调拨需求：", res)
            return res.get("data")
        else:
            log.error(res)
            return


if __name__ == '__main__':
    wms_service = WmsServiceController()
    kw = {
            "deliveryWarehouseCode": "UKBH01", "deliveryTargetWarehouseCode": "",
            "receiveWarehouseCode": "UKBH02", "receiveTargetWarehouseCode": "",
            "demandType": 2, "goodsSkuCode": "53586714577", "bomVersion": "C"
    }
    res = wms_service.service_demand_create(**kw)
    print(res)
    demand_code = res.get("data")["demandCode"]

    # kw = {"demandCode": "demand_code"}
    # kw = {"demandCode": "XQ2303150002"}
    # res = wms_service.service_demand_cancel(**kw)