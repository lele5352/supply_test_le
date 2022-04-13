from controller.wms_controller import WmsController
from controller.stockoperation_controller import StockOpearationController
from controller.oms_controller import OmsController
from controller.pda_controller import PdaController
from config.sys_config import env_config
from data_maker import *
import time


class TransferMaker:
    def __init__(self):
        self.prefix = env_config.get("app_prefix")
        self.time_tamp = int(time.time() * 1000)
        self.wms = WmsController(ums)
        self.st = StockOpearationController(ums)
        self.oms = OmsController(ums)
        self.pda = PdaController(ums)
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
                      receive_target_warehouse_code, num, skucode, sku_type, delivery_kw_tp_code_list, receive_kw_sj_code_list):
        # 切换到发货仓库
        self.wms.switch_warehouse(delivery_warehouse_code)
        # 获取调拨需求sku相关信息
        sku_list = self.oms.list_sku(sku_type, skucode)
        sku_info = sku_list.get("data")["records"]

        # 新增调拨需求
        # self.oms.demand_create(delivery_warehouse_code, delivery_target_warehouse_code, receive_warehouse_code,
        #               receive_target_warehouse_code, sku_info, num)

        #查询调拨需求请求参数
        kw = {
            "states": [0],
            # "startCreateTime": self.time_tamp - 5000,  #查询5秒内的sku
            # "endCreateTime": self.time_tamp,
            "createUserId": 10
        }
        # 查询最近3秒生成的调拨需求列表
        demands = self.wms.demand_list(**kw)
        # 获取调拨需求列表
        demands_list = demands.get("data")["records"]
        # 获取调拨需求相关的信息
        demands_info = self.wms.demand_info(demands_list)
        # 新增调拨拣货单
        res = self.wms.picking_create(demands_info)
        # 获取调拨拣货单号
        pick_order_no = res.get("data")
        # 分配拣货人
        self.wms.assign_pick_user(pick_order_no)
        # 获取拣货单信息
        picking_info = self.wms.picking_detail(pick_order_no)
        # 确认拣货--当前是完全拣货
        self.wms.do_picking(pick_order_no, picking_info)

        # PDA-按需装托时，扫码拣货单号，获取拣货单信息
        info = self.pda.pda_picking_detail(pick_order_no)
        picking_detail_info = info.get("data")

        # 按需装托
        self.pda.pda_submit_tray_info(delivery_kw_tp_code_list, picking_detail_info)

        # 创建出库单以及生成箱单
        res = self.pda.pda_finish_picking(pick_order_no, delivery_kw_tp_code_list)
        # 创建出库单结果： {'code': 200, 'message': '操作成功', 'data': 'DC2204120031'}
        transfer_out_no = res.get("data")

        # 查询调拨出库单下的箱单列表
        kw = {
            "transferOutNos": [transfer_out_no],
        }
        res = self.wms.search_box_out_list(**kw)
        box_no_list = res.get("data")["records"]

        # 调拨复核
        for i in box_no_list:
            self.pda.pda_review_submit(i.get("boxNo"), i.get("storageLocationCode"))
        # 调拨发货交接
        for i in box_no_list:
            res = self.pda.pda_handover_bind(i.get("boxNo"))
        handover_no = res.get("data")["handoverNo"]
        # 调拨发货
        self.pda.pda_delivery_confirm(handover_no)


        # 切换到收货仓库货仓库
        self.wms.switch_warehouse(receive_warehouse_code)
        #调拨入库--确认收货
        self.pda.pda_transfer_in_confirm(handover_no)
        kw_box_in = {
            "handoverNo": handover_no,
        }
        # 调拨入库-整箱上架
        res = self.pda.wms.search_box_in_list(**kw_box_in)
        box_no_info = res.get("data")["records"]
        for i in box_no_info:
            self.pda.pda_transfer_in_receive_all(i.get("boxNo"), receive_kw_sj_code_list[0], i.get("transferInNo"))







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
    transfer.transfer_maker("UKBH01", "", "UKBH02", "", 1, "53586714577", 1, ["KW-RQ-TP-01"], ["KW-SJQ-01"])