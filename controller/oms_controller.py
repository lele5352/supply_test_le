from config.api_config.oms_api import oms_api_config
from config.api_config.wms_api import wms_api_config
from config.sys_config import env_config
from tools.request_operator import RequestOperator
from controller.ums_controller import UmsController


class OmsController(RequestOperator):
    def __init__(self):
        self.prefix = env_config.get("app_prefix")
        self.headers = UmsController().get_app_headers()
        super().__init__(self.prefix, self.headers)


    def get_warehouses_list(self):
        # timestamp = int(time.time()) * 1000
        oms_api_config.get("get_warehouses_list")["data"].update({
            "t": self.time_tamp
        })
        res = self.send_request(**oms_api_config.get("get_warehouses_list"))
        # print(res)
        return res.get("data")


    def get_warehouse_info(self, warehouse_code):
        """
        :param warehouse_code: 仓库code
        :return: 仓库信息，包含：{"id": xxx, "warehouse_id":xxx, "warehouse_name":xxx, "warehouse_code":xxx}
        """
        warehouses_list = self.get_warehouses_list()
        for i in warehouses_list:
            if warehouse_code == i["warehouseCode"]:
                warehouse_info = {
                    "warehouseId": i["warehouseId"],
                    "warehouseName": i["warehouseName"],
                    "warehouseCode": i["warehouseCode"],
                }
        return warehouse_info

    def list_sku(self, type, skucode):
        """
        :param type: 1-销售sku，2-部件
        :param saleskucode:可以为销售sku，也可以为仓库sku
        :return: sku_info:sku信息
        """
        oms_api_config.get("list_product")["data"].update({
            "type": type,
            "skuCode": skucode,
            "t": self.time_tamp,
        })
        try:
            res = self.send_request(**oms_api_config.get("list_product"))
            print(res.get("data")["records"])
        except Exception as e:
            raise Exception('err_info:{}'.format(e))
        return res.get("data")["records"]

    def demand_create(self, delivery_warehouse_code, delivery_target_warehouse_code, receive_warehouse_code,
                      receive_target_warehouse_code, sku_info, num):
        """

        :param delivery_warehouse_code: 发货仓
        :param delivery_target_warehouse_code: 发货仓目的仓
        :param receive_warehouse_code: 收货仓
        :param receive_target_warehouse_code: 收货仓目的仓
        :param sku_info: 类型为list，sku信息
        :param num:数量
        :return:
        """
        delivery_warehouse_info = self.get_warehouse_info(delivery_warehouse_code)
        receive_warehouse_info = self.get_warehouse_info(receive_warehouse_code)

        if delivery_target_warehouse_code:
            delivery_target_warehouse_id = None
            delivery_target_warehouse_code = None
            delivery_target_warehouse_name = None
        else:
            delivery_target_warehouse_info = self.get_warehouse_info(delivery_target_warehouse_code)
            delivery_target_warehouse_id = delivery_target_warehouse_info.get("warehouseId")
            delivery_target_warehouse_code = delivery_target_warehouse_info.get("warehouseCode")
            delivery_target_warehouse_name = delivery_target_warehouse_info.get("warehouseName")
        if receive_target_warehouse_code:
            receive_target_warehouse_id = None
            receive_target_warehouse_code = None
            receive_target_warehouse_name = None
        else:
            receive_target_warehouse_info = self.get_warehouse_info(receive_target_warehouse_code)
            receive_target_warehouse_id = receive_target_warehouse_info.get("warehouseId")
            receive_target_warehouse_code = receive_target_warehouse_info.get("warehouseCode")
            receive_target_warehouse_name = receive_target_warehouse_info.get("warehouseName")

        oms_api_config.get("demand_create").update({
            "deliveryWarehouseId": delivery_warehouse_info.get("warehouseId"),
            "deliveryWarehouseName": delivery_warehouse_info.get("warehouseName"),
            "deliveryWarehouseCode": delivery_warehouse_info.get("warehouseCode"),
            "deliveryTargetWarehouseId": delivery_target_warehouse_id,
            "deliveryTargetWarehouseName": delivery_target_warehouse_name,
            "deliveryTargetWarehouseCode": delivery_target_warehouse_code,
            "receiveWarehouseId": receive_warehouse_info.get("warehouseId"),
            "receiveWarehouseName": receive_warehouse_info.get("warehouseName"),
            "receiveWarehouseCode": receive_warehouse_info.get("warehouseCode"),
            "receiveTargetWarehouseName": receive_target_warehouse_name,
            "receiveTargetWarehouseCode": receive_target_warehouse_code,
            "receiveTargetWarehouseId": receive_target_warehouse_id,
            "details": {
                "itemSkuCode": sku_info[0]["skuCode"],
                "itemSkuType": sku_info[0]["type"],
                "quantity": num,
                "itemPicture": sku_info[0]["mainUrl"]
            }
        })
        try:
            print(oms_api_config.get("demand_create"))
            res = self.send_request(**oms_api_config.get("demand_create"))
            print(res)
        except Exception as e:
            print(Exception("err_info:{}".format(e)))
            raise (Exception("err_info:{}".format(e)))


if __name__ == '__main__':
    oms = OmsController()
    # oms.list_sku(1, "53586714577")
    sku_info = [{"skuCode": "53586714577", "productNameCn": "决明子", "type": 1, "typeName": "销售sku", "relateSku": None, "categoryName": "家具>家具套装>餐桌桌椅套装", "mainUrl": "https://img.popicorns.com/dev/file/2021/11/08/8cbba5e1160a48e9bd9b43e54450ab7c.jpg"}]
    oms.demand_create("UKBH01"," ","UKBH02"," ",sku_info,1)