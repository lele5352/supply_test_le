from config.api_config.oms_api import oms_api_config
from config.sys_config import env_config
from tools.request_operator import RequestOperator
from controller.ums_controller import UmsController


class OmsController(RequestOperator):
    def __init__(self, ums):
        self.prefix = env_config.get("app_prefix")
        self.headers = ums.header
        super().__init__(self.prefix, self.headers)

    # 获取仓库列表
    def get_warehouses_list(self):
        # timestamp = int(time.time()) * 1000
        oms_api_config.get("get_warehouses_list")["data"].update({
            "t": self.time_tamp
        })
        res = self.send_request(**oms_api_config.get("get_warehouses_list"))
        # print(res)
        return res.get("data")

    # 获取仓库相关信息包含：id、code、name
    def get_warehouse_info(self, warehouse_code):
        """
        :param warehouse_code: 仓库code
        :return: 仓库信息，包含：{"warehouseId":xxx, "warehouseName":xxx, "warehouseCode":xxx}
        """
        warehouses_list = self.get_warehouses_list()
        warehouse_info = {}
        for i in warehouses_list:
            if warehouse_code == "":
                return warehouse_info
            elif warehouse_code == i["warehouseCode"]:
                warehouse_info = {
                    "warehouseId": i["warehouseId"],
                    "warehouseName": i["warehouseName"],
                    "warehouseCode": i["warehouseCode"],
                }
                return warehouse_info
        print("err_info：无此仓库编码！")

    # 新增调拨需求时，获取sku相关数据信息
    def list_sku(self, skutype, skucode):
        """
        :param type: 1-销售sku，2-部件
        :param saleskucode:可以为销售sku，也可以为仓库sku
        :return: sku_info:sku信息
        """
        oms_api_config.get("list_product")["data"].update({
            "type": skutype,
            "skuCode": skucode,
            "t": self.time_tamp,
        })
        try:
            res = self.send_request(**oms_api_config.get("list_product"))
            print(res.get("data")["records"])
            return res
        except Exception as e:
            raise Exception('err_info:', e)


    # 新增调拨需求
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
        #获取调拨相关仓库信息
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

        details = []
        #组装调拨需求sku相关信息参数
        for item in sku_info:
            sku_detail = {
                "itemSkuCode": item["skuCode"],
                "itemSkuType": item["type"],
                "quantity": num,
                "itemPicture": item["mainUrl"]
            }
            details.append(sku_detail)

        oms_api_config.get("demand_create")["data"].update({
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
            "details": details
        })
        try:
            res = self.send_request(**oms_api_config.get("demand_create"))
            print(res)
        except Exception as e:
            raise (Exception("err_info:", e))




if __name__ == '__main__':
    ums = UmsController()
    oms = OmsController(ums)
    # oms.list_sku(1, "53586714577")
    sku_info = [{"skuCode": "53586714577", "productNameCn": "决明子", "type": 1, "typeName": "销售sku", "relateSku": None, "categoryName": "家具>家具套装>餐桌桌椅套装", "mainUrl": "https://img.popicorns.com/dev/file/2021/11/08/8cbba5e1160a48e9bd9b43e54450ab7c.jpg"}]
    oms.demand_create("UKBH01", "", "UKBH02", "", sku_info, 2)
