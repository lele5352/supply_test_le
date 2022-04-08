from controller.wms_controller import WmsController
from controller.stockoperation_controller import StockOpearationController
from controller.oms_controller import OmsController
from config.sys_config import env_config
from data_maker import *
import time


class TransferMaker:
    def __init__(self):
        self.prefix = env_config.get("app_prefix")
        self.time_tamp = int(time.time()) * 1000
        self.wms = WmsController(ums)
        self.st = StockOpearationController(ums)
        self.oms = OmsController(ums)
        # super().__init__(self.prefix, self.headers)


    def add_other_stock(self, warehouse_code, salesku, bom_ver, skunum, shelves_location_code):
        # 切换到相关仓库
        self.wms.switch_warehouse(warehouse_code)
        # 获取入库单信息
        entryorder_info = self.wms.entryorder(salesku, bom_ver, skunum)
        # 获取入库单sku列表信息
        entryorder_sku_list = self.wms.get_sku_info_by_entryCode(entryorder_info)
        # 获取入库单id
        entryo_order_id = entryorder_info.get("entryOrderId")
        # 请求上架接口
        res = self.wms.put_on_the_shelf(shelves_location_code, skunum, entryo_order_id, entryorder_sku_list)
        print("上架操作：", res)

    def add_adjust_stock(self, warehouse_code, adjust_sku_info, status, change_type, source):
        """

        :param warehouse_code: 仓库编码
        :param adjust_sku_info: 调整的sku信息
        :param status: 查询条件--状态：null-全部，1-待审核，2-已审核，3-已驳回
        :param change_type: 变动类型 0-全部，1-盘亏，2-盘盈
        :param source: 来源：0-全部，1-人工创建，2-短拣异常
        :return:
        """
        # 切换到相关仓库
        self.wms.switch_warehouse(warehouse_code)
        # 创建调整单
        self.st.adjust_receipt(adjust_sku_info)
        # 查询调整单信息，获取调整单ids
        adjust_orders = self.st.adjust_receipt_page(status, change_type, source)
        ids = []
        for i in adjust_orders:
            ids.append(i.get("id"))
        print(ids)
        # 审核调整单
        pass

    def transfer_maker(self, delivery_warehouse_code, delivery_target_warehouse_code, receive_warehouse_code,
                      receive_target_warehouse_code, num, skucode, sku_type):
        # 切换到相关仓库
        self.wms.switch_warehouse(delivery_warehouse_code)
        # 查获取调拨需求sku相关信息
        sku_list = self.oms.list_sku(sku_type, skucode)
        sku_info = sku_list.get("data")["records"]

        # 新增调拨需求
        self.oms.demand_create(delivery_warehouse_code, delivery_target_warehouse_code, receive_warehouse_code,
                      receive_target_warehouse_code, sku_info, num)







if __name__ == '__main__':
    transfer = TransferMaker()
    #其他入库
    # transfer.add_other_stock("UKBH01", "53586714577", ["G", "F"], 3, "KW-SJQ-01")     #其他入库添加库存
    """
    # 调整单
    transfer.add_adjust_stock("UKBH01",
                              [{"waresSkuCode": "53586714577B01",
                                "storageLocationCode": "KW-SJQ-01",
                                "changeCount": "1",
                                "changeType": "2",
                                "adjustReason": "2"}],
                              1, 0, 1)
    """
    # 新增调拨需求
    transfer.transfer_maker("UKBH01", "", "UKBH02", "", 1)