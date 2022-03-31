from tools.request_operator import RequestOperator
from tools.mysql_operator import MySqlOperator
from config.sys_config import env_config
from controller.ums_controller import UmsController
from config.api_config.wms_api import wms_api_config
import time

class WmsController(RequestOperator):

    def __init__(self):
        self.prefix = env_config.get("app_prefix")
        self.headers = UmsController().get_app_headers()
        super().__init__(self.prefix, self.headers)

        self.db = MySqlOperator(**env_config.get("mysql_info_ims"))


    def get_warehouses_list(self):
        # timestamp = int(time.time()) * 1000
        wms_api_config.get("get_warehouses_list")["data"].update({
            "t": self.time_tamp
        })
        res = self.send_request(**wms_api_config.get("get_warehouses_list"))
        # print(res)
        return res.get("data")

    def get_warehouse_info(self, warehouse_code):
        """
        :param warehouse_code: 仓库code
        :return: 仓库信息，包含：{"id": xxx, "warehouse_id":xxx, "warehouse_name":xxx, "warehouse_code":xxx}
        """
        warehouses_list = self.get_warehouses_list()
        for i in warehouses_list:
            if warehouse_code == i["ext"]["warehouseCode"]:
                warehouse_info = {
                    "warehouseId": i["ext"]["warehouseId"],
                    "warehouseName": i["ext"]["warehouseName"],
                    "warehouseCode": i["ext"]["warehouseCode"],
                    "id": i["id"]
                }
        return warehouse_info

    def switch_warehouse(self, warehouse_code):
        """
        :param warehouse_code: 仓库code
        :return:
        """
        warehouse_info = self.get_warehouse_info(warehouse_code)
        wms_api_config.get("switch_warehouse")["data"].update({"dataPermId": warehouse_info.get("id")})
        res = self.send_request(**wms_api_config.get("switch_warehouse"))
        return res

    def other_add_skuinfo_page(self, skucode):
        """
        :param skucode: 仓库sku
        :return:
        """
        wms_api_config.get("other_add_skuinfo_page")["data"].update({"skuCodeLike": skucode})
        res = self.send_request(**wms_api_config.get("other_add_skuinfo_page"))
        return res.get("data").get("records")

    def entryorder(self, sku_code, bom_version, num, operation_flag=1):
        """
        :param sku_code: 仓库sku
        :param bom_version: BOM版本
        :param num: 入库套数
        :param operation_flag: 其他入库单状态：1已提交  0暂存，默认值为：1
        :return: 字典类型的入库单信息，包含：{"entryorderId" : xxx,"entryorderCode": xxx}
        """
        sku_info = self.other_add_skuinfo_page(sku_code)

        sku_list = []
        for i in sku_info:
            if i.get("bomVersion") in bom_version:
                sku_list.append(i)
        for i in sku_list:
            del i["sort"]
            del i["volume"]
            bom_num = int(i.get("skuName")[-1])
            i.update({"planSkuQty": (bom_num * num)})
            i["warehouseSkuCode"] = i.pop("skuCode")
            i["warehouseSkuName"] = i.pop("skuName")
            i["saleSkuCode"] = i.pop("saleSku")
            i["saleSkuName"] = i.pop("skuZhName")
            i["saleSkuImg"] = i.pop("skuImageUrl")
            i["warehouseSkuWeight"] = i.pop("weight")

        timestamp = int(time.time()) * 1000
        wms_api_config.get("entryorder")["data"].update({"skuInfoList": sku_list, "eta": timestamp, "timestamp": timestamp, "operationFlag": operation_flag})
        res = self.send_request(**wms_api_config.get("entryorder"))
        entryorder_info = res.get("data")
        return entryorder_info

    def get_sku_info_by_entryCode(self, entryorder_info):
        """

        :param entryorder_info: 入库单相关信息，包含：entryorderId、entryorderCode
        :return: 入库单内的sku列表信息
        """
        wms_api_config.get("get_sku_info_by_entryCode")["data"].update(entryorder_info)
        res = self.send_request(**wms_api_config.get("get_sku_info_by_entryCode"))
        entryorder_sku_list = res.get("data")["records"]
        return entryorder_sku_list

    def get_entry_order_by_id(self, entryo_order_id):
        """
        获取其他入库单相关信息
        :param entryo_order_id: 入库单id
        :return: 入库单相关单据信息
        """
        timestamp = int(time.time()) * 1000
        uri_path_prefix = wms_api_config.get("get_entry_order_by_id")["uri_path"]
        wms_api_config.get("get_entry_order_by_id")["data"].update({"t": timestamp})
        wms_api_config.get("get_entry_order_by_id")["uri_path"] = uri_path_prefix + entryo_order_id
        res = self.send_request(**wms_api_config.get("get_entry_order_by_id"))
        return res.get("data")

    def put_on_the_shelf(self, shelves_location_code, skuqty, entryo_order_id, entryorder_sku_list):
        """
        其他入库上架
        :param shelves_location_code: 上架库位code
        :param skuqty: 上架数量
        :param entryo_order_id: 其他入库单id
        :param skulist: 上架的sku列表
        :return:
        """
        sku_list = []
        for i in entryorder_sku_list:
            x = {
                "shelvesLocationCode": shelves_location_code,
                "skuQty": skuqty * (int(i["warehouseSkuLabel"][-1])),
                "skuCode": i["warehouseSkuCode"],
                "abnormalQty": 0
            }
            sku_list.append(x)
        wms_api_config.get("put_on_the_shelf")["data"].update({"entryOrderId": entryo_order_id, "skuList": sku_list})
        res = self.send_request(**wms_api_config.get("put_on_the_shelf"))
        return res.get("message")

    def del_wares(self):
        sql_ims_list = [
            "DELETE FROM wares_inventory WHERE goods_sku_code = '53586714577';",
            "DELETE FROM goods_inventory WHERE goods_sku_code = '53586714577' ;",
            "DELETE FROM central_inventory WHERE goods_sku_code = '53586714577';",
        ]

        # sql_wms_list = [
        #     "DELETE FROM trf_transfer_out_order WHERE warehouse_id =536;",
        #     "DELETE FROM trf_transfer_out_order_detail WHERE warehouse_id =536;",
        #     "DELETE FROM trf_transfer_in_order WHERE warehouse_id =517;",
        #     "DELETE FROM trf_transfer_in_order_detail WHERE warehouse_id =536;",
        #     "DELETE FROM trf_box_order WHERE warehouse_id =536;",
        #     "DELETE FROM trf_box_order_detail WHERE warehouse_id =536;",
        #     "DELETE FROM trf_box_order_in WHERE warehouse_id =517;",
        #     "DELETE FROM trf_box_order_detail_in WHERE warehouse_id =536;",
        #     "DELETE FROM trf_handover_order WHERE warehouse_id =536;",
        #     "DELETE FROM trf_transfer_demand WHERE warehouse_id =536;",
        #     "DELETE FROM trf_transfer_pick_order WHERE warehouse_id =536;",
        #     "DELETE FROM trf_transfer_pick_order_detail WHERE warehouse_id = 536;"
        # ]

        # sql = "select * from wares_inventory where goods_sku_code = '53586714577';"
        # data = self.db.get_sql_all(sql)
        for i in sql_ims_list:
            self.db.executemany(i)
        self.db.close()

        print("清理数据完成")


    def sdf(self):
        pass



if __name__ == '__main__':
    wms = WmsController()
    # wms.get_warehouses_list()
    # wms.switch_warehouse("UKBH01")
    # wms.entryorder("53586714577", ["B"], 2)

    # wms.get_sku_info_by_entryCode(wms.entryorder("53586714577", ["B", "D"], 5))
    # wms.get_entry_order_by_id("1843")
    wms.del_wares()