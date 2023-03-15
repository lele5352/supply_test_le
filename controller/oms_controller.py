import time
from config.api_config.oms_api import oms_api_config
from tools.request_operator import RequestOperator
from controller import *


class OmsController(RequestOperator):
    def __init__(self):
        self.prefix = web_prefix
        self.headers = app_headers
        super().__init__(self.prefix, self.headers)

    # 获取仓库列表
    def get_warehouses_list(self):
        oms_api_config.get("get_warehouses_list")["data"].update({
            "t": self.time_tamp
        })
        res = self.send_request(**oms_api_config.get("get_warehouses_list"))
        return res.get("data")

    # 获取仓库相关信息包含：id、code、name
    def get_warehouse_info(self, warehouse_code):
        """
        :param warehouse_code: 仓库code
        :return: 仓库信息，包含：{"warehouseId":xxx, "warehouseName":xxx, "warehouseCode":xxx}
        """
        warehouses_list = self.get_warehouses_list()

        if warehouse_code == "":
            print("err_info：必填项-仓库编码不能为空！")
            return
        for i in warehouses_list:
            if warehouse_code == i["warehouseCode"]:
                warehouse_info = {
                    "warehouseId": i["warehouseId"],
                    "warehouseName": i["warehouseName"],
                    "warehouseCode": i["warehouseCode"],
                }
                return warehouse_info
            else:
                continue
        print("err_info：无此仓库编码！")
        return


    # 新增调拨需求时，获取sku相关数据信息----废除不再使用
    def list_sku(self, skutype, skucode):
        """
        :param skutype: 1-销售sku，2-部件
        :param saleskucode:可以为销售sku，也可以为仓库sku
        :param bomversion:bom版本
        :return: sku_info:sku信息
        """
        oms_api_config.get("list_product")["data"].update({
            "type": skutype,
            "skuCode": skucode,
            "t": self.time_tamp,
        })
        try:
            res = self.send_request(**oms_api_config.get("list_product"))
            # print(res.get("data")["records"])
            return res.get("data")["records"]
        except Exception as e:
            raise Exception('err_info:', e)


    # 新增调拨需求--新
    def demand_create(self, delivery_warehouse_code, delivery_target_warehouse_code, receive_warehouse_code,
                      receive_target_warehouse_code, sku_list):
        """

        @param delivery_warehouse_code: 发货仓编码
        @param delivery_target_warehouse_code: 发货仓目的仓编码
        @param receive_warehouse_code: 收货仓编码
        @param receive_target_warehouse_code: 收货仓目的仓编码
        @param sku_list: 格式举例：[{"code": "53586714577",
                                 "type": 1,  #1-销售sku   2-部件sku
                                 "bom_version": "F",    #bom版本
                                 "num": 1   #数量
                                 }]
        @return:
        """

        # 获取调拨相关仓库信息
        delivery_warehouse_info = self.get_warehouse_info(delivery_warehouse_code)
        receive_warehouse_info = self.get_warehouse_info(receive_warehouse_code)
        if delivery_target_warehouse_code:
            delivery_target_warehouse_info = self.get_warehouse_info(delivery_target_warehouse_code)
            delivery_target_warehouse_id = delivery_target_warehouse_info.get("warehouseId")
            delivery_target_warehouse_code = delivery_target_warehouse_info.get("warehouseCode")
            delivery_target_warehouse_name = delivery_target_warehouse_info.get("warehouseName")
        else:
            delivery_target_warehouse_id = None
            delivery_target_warehouse_code = None
            delivery_target_warehouse_name = None

        if receive_target_warehouse_code:
            receive_target_warehouse_info = self.get_warehouse_info(receive_target_warehouse_code)
            receive_target_warehouse_id = receive_target_warehouse_info.get("warehouseId")
            receive_target_warehouse_code = receive_target_warehouse_info.get("warehouseCode")
            receive_target_warehouse_name = receive_target_warehouse_info.get("warehouseName")

        else:
            receive_target_warehouse_id = None
            receive_target_warehouse_code = None
            receive_target_warehouse_name = None

        details = []
        # 组装调拨需求sku相关信息参数
        for i in sku_list:
            skutype = i.get("type")
            code = i.get("code")
            bom_version = i.get("bom_version")
            sku_msg = self.list_sku(skutype, code)
            if skutype == 1:
                sku_detail = {
                    "itemSkuCode": sku_msg[0]["skuCode"],
                    "itemSkuType": sku_msg[0]["type"],
                    "quantity": i.get("num"),
                    "itemPicture": sku_msg[0]["mainUrl"],
                    "bomVersion": bom_version
                }
                details.append(sku_detail)
                continue
            elif skutype == 2:
                for item in sku_msg:
                    if item.get("mostBomVersion") == bom_version:
                        sku_detail = {
                            "itemSkuCode": item["skuCode"],
                            "itemSkuType": item["type"],
                            "quantity": i.get("num"),
                            "itemPicture": item["mainUrl"],
                            "bomVersion": bom_version
                        }
                        details.append(sku_detail)
                        break
            else:
                print("sku_info列表为空：", sku_msg)
        remark = "DBXQ{0}".format(int(time.time()))
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
            "details": details,
            "remark": remark
        })
        try:
            res = self.send_request(**oms_api_config.get("demand_create"))
            print("新增调拨需求：", res)
            return remark
        except Exception as e:
            raise (Exception("err_info:", e))


    def demand_page(self, remark):
        oms_api_config.get("demand_page")["data"].update({
            "remark": remark
        })
        try:
            res = self.send_request(**oms_api_config.get("demand_page"))
            print("OMS侧查询调拨需求信息：", res)
            return res
        except Exception as e:
            raise (Exception("err_info:", e))


    def cancel_demand(self, id):
        oms_api_config.get("cancel_demand")["data"].update(
            {
                "id": id
            }
        )
        try:
            res = self.send_request(**oms_api_config.get("cancel_demand"))
            print("取消调拨需求：", res)
        except Exception as e:
            raise (Exception("err_info:", e))






if __name__ == '__main__':

    oms = OmsController()
    # oms.list_sku(2, "53586714577")
    sku_list = [
         {
            "code": "70076739388",
            "type": 1,
            "bom_version": "C",
            "num": 3
         },
        {
            "code": "70076739388",
            "type": 2,
            "bom_version": "C",
            "num": 2
         }
        ]
    remark = oms.demand_create("LELE-ZZ", "LELE-ZF", "LELE-ZF", "", sku_list)
    # remark = "DBXQ1658222471"
    # res = oms.demand_page(remark)
    # oms_demand_list = res.get("data")["records"]

    # oms.cancel_demand(751)
    # oms.get_warehouse_info("UKBH01")