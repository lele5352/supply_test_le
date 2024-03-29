from data_maker import *
import time
class WmsMaker:
    def __init__(self):
        self.time_tamp = int(time.time() * 1000)
        self.wms = wms
        self.st = st
        self.oms = oms
        self.pda = pda
        self.wms_service_robot = wms_service_robot

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
        调整单--新增
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
                       receive_target_warehouse_code, goods_sku_code, demand_qty, bom_version, delivery_kw_tp_code_list,
                       receive_kw_sj_code_list):
        """
        # 切换到发货仓库
        self.wms.switch_warehouse(delivery_warehouse_code)


        # 新增调拨需求--返回备注字段信息
        demand_code = self.wms_service_robot.transfer_demand_creat(delivery_warehouse_code,
                                                                   delivery_target_warehouse_code,
                                                                   receive_warehouse_code,
                                                                   receive_target_warehouse_code,
                                                                   goods_sku_code, demand_qty, bom_version)

        # demand_code = ["XQ2311090054"]
        # 查询调拨需求请求参数
        kw = {
            "demandCodeList": [demand_code],
            # "demandCodeList": demand_code#临时用
        }
        print(kw)
        
        # 查询生成的调拨需求列表
        res = self.wms.demand_list(**kw)
        # 获取调拨需求相关信息
        demands_info = res.get("data")["records"]

        # 新增调拨拣货单
        res = self.wms.picking_create(demands_info)
        # 获取调拨拣货单号
        pick_order_no = res.get("data")

        # pick_order_no = 'DJH2309150005'
        # 分配拣货人
        self.wms.assign_pick_user(pick_order_no)

        # 获取拣货单信息
        picking_info = self.wms.picking_detail(pick_order_no)

        # 确认拣货--当前是完全拣货
        self.wms.do_picking(pick_order_no, picking_info)

        # pick_order_no = 'DJH2301100007'
        # PDA-按需装托时，扫码拣货单号，获取拣货单信息
        info = self.pda.pda_picking_detail(pick_order_no)
        picking_detail_info = info.get("data")

        # 按需装托
        # 按需装托在单个库位上
        self.pda.pda_submit_tray_info(delivery_kw_tp_code_list, picking_detail_info)
        # 按需装托在多个库位上
        # self.pda.pda_submit_tray_info_many(delivery_kw_tp_code_list, picking_detail_info)

        # pick_order_no = 'DJH2311100092'
        # 创建出库单以及生成箱单
        res = self.pda.pda_finish_picking(pick_order_no, delivery_kw_tp_code_list)
        # 创建出库单结果： {'code': 200, 'message': '操作成功', 'data': 'DC2204120031'}
        transfer_out_no = res.get("data")

        # transfer_out_no = "DC2311100092"
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
        handover_ids = [res.get("data")["id"]]

        # 调拨发货-维护物流
        self.pda.pda_logistics_update(handover_ids)
        # 调拨发货-发货
        self.pda.pda_delivery_confirm(handover_no)

        """
        handover_no = "DBJJ2311130004"
        # 切换到收货仓库货仓库
        self.wms.switch_warehouse(receive_warehouse_code)
        # 调拨入库--确认收货
        self.pda.pda_transfer_in_confirm(handover_no)

        kw_box_in = {
            "handoverNo": handover_no,
        }
        res = self.pda.wms.search_box_in_list(**kw_box_in)
        box_no_info = res.get("data")["records"]
        list_info = []
        # for i in box_no_info:
        #     list_info.append(i.get("boxNo"))
        #     box_info = self.pda.pda_transfer_in_box_scan(i.get("boxNo"))
        
        # 调拨入库-整箱上架
        for i in box_no_info:
            self.pda.pda_transfer_in_receive_all(i.get("boxNo"), receive_kw_sj_code_list[0], i.get("transferInNo"))
        # """

    def cj_transfer_maker(self, delivery_warehouse_code, receive_warehouse_code, sku_info_list,
                          receive_kw_sj_code_list):
        # """
        # 切换到发货仓库
        self.wms.switch_warehouse(delivery_warehouse_code)

        # 获取即将新增仓间调拨的sku_code列表
        sku_code_list = []
        for i in sku_info_list:
            sku_code_list.append(i.get("sku_code"))
        # 传入sku_code列表查询相关sku信息
        res = self.wms.cj_sku_info_page(sku_code_list)
        cj_sku_info = res.get("data")["records"][0]["skuList"]
        # 组装仓间调拨时要用到的sku信息及数量
        sku_items = []
        for j in cj_sku_info:
            for z in sku_info_list:
                if z.get("sku_code") == j.get("skuCode"):
                    item = {
                        "locationCode": j.get("warehouseLocationCode"),
                        "skuCode": j.get("skuCode"),
                        "skuQty": z.get("num")
                    }
                    sku_items.append(item)
        remark = "自动化_CJ{0}".format(int(time.time()))
        # 新增仓间调拨
        res = self.wms.cj_create_inner(receive_warehouse_code, sku_items, remark)

        # 新增的仓间调拨单相关信息存储下来
        pick_order_no = res.get("data")["pickOrderNo"]
        instruct_order_id = res.get("data")["instructOrderId"]
        search_cj = {
            "pickOrderNo": [pick_order_no]
        }
        # 仓间调拨-查询仓间调拨出库页面
        res = self.wms.cj_platform_transferout_page(**search_cj)
        transfer_out_id = res.get("data")["records"][0]["transferOutId"]
        pick_order_id = res.get("data")["records"][0]["pickOrderId"]

        # 仓间调拨-查看出库单详情页,获取pick_details详情,并修改实拣数量为待拣数量
        res = self.wms.cj_detail_page(transfer_out_id)
        pick_details = res.get("data")["pickDetails"]
        for i in pick_details:
            i["pickQty"] = i.get("skuQty")
        # 仓间调拨-确认拣货
        self.wms.cj_confirmPick(pick_order_id, pick_order_no, pick_details)
        # 仓间调拨-发货
        res = self.wms.cj_deliver_inner(instruct_order_id)
        handover_no = res.get("data")["handoverOrderNo"]
        # """

        # 切换到收货仓库货仓库
        # handover_no = "CJJJ2309060001"
        self.wms.switch_warehouse(receive_warehouse_code)
        # 调拨入库--确认收货
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
    transfer = WmsMaker()

    # 调整单
    """
    transfer.add_adjust_stock("UKBH01",
                              [{"waresSkuCode": "53586714577B01",
                                "storageLocationCode": "KW-SJQ-01",
                                "changeCount": "1",
                                "changeType": "2",
                                "adjustReason": "2"}],
                              1, 0, 1)
    """

    # 其他入库
    # transfer.add_other_stock("USLA01", "53586714577", ["C"], 20, "SJ")     #其他入库添加库存
    # transfer.add_other_stock("UKBH01", "53586714577", ["C"], 5, "KW-SJQ-01")
    # transfer.add_other_stock("LELE-BH", "94991138113", ["A"], 2, "KW-SJQ-01")  #189环境
    # transfer.add_other_stock("FSBH02", "71230293819", ["C"], 5, "KW-SJQ-01")  # UAT环境--其他入库添加库存

    sku_list = [
        {
            "code": "53586714577",  # JFW28445H5B01  J011194-2VA01    JF5891A6J4A01    53586714577C01
            "type": 1,
            "bom_version": "C",
            "num": 2
        }
    ]
    # 160环境
    # transfer.transfer_maker("PBZZ", "PBTS", "PBTS", "PBTS", "P37727418", 3, "A", ["KW-RQ-TP-01"], ["KW-SJQ-01"])
    # transfer.transfer_maker("0517-1", "", "0517-3", "", "53586714577", 1, "C",  ["KW-RQ-TP-01"], ["KW-SJQ-01"])
    # transfer.transfer_maker("LELE-BH", "", "LELE-ZF", "LELE-ZF", "HW9493FU49", 5, "D",  ["KW-RQ-TP-01"], ["KW-SJQ-01"])
    # transfer.transfer_maker("LELE-BH", "", "PPBH", "", "53586714577", 3, "C",  ["KW-RQ-TP-01", "KW-RQ-TP-02"], ["KW-SJQ-01"])
    transfer.transfer_maker("LELE-BH", "", "LELE-ZF", "LELE-ZF", "HW9493FU49", 3, "A",  ["KW-RQ-TP-01",
                                                                                          "KW-RQ-TP-02"], ["KW-SJQ-01"])
    # transfer.transfer_maker("LELE-ZF", "LELE-ZF", "LELE-ZF1", "LELE-ZF1", "HW6526W5Y5", 10, "A",  ["KW-RQ-TP-01",
    #                                                                                        "KW-RQ-TP-02"],["KW-SJQ-01"])

    # 189环境
    # transfer.transfer_maker("KWDR-TEST", "", "LELE-BH", "", sku_list, ["KW-RQ-TP-01", "KW-RQ-TP-02", "KW-RQ-TP-03"], ["KW-SJQ-01"])
    # transfer.transfer_maker("LELE-ZZ", "LELE-ZF", "LELE-ZF", "", sku_list, ["KW-RQ-TP-01","KW-RQ-TP-03"], ["KW-SJQ-01"])
    # 新增调拨需求--uat环境
    # transfer.transfer_maker("FSBH02", "", "CA01", "", 2, "71230293819", 1, ["KW-RQ-TP-01"], ["KW-SJQ-01"])

    # 新增仓间调拨
    sku_info_list = [
        {"sku_code": "53586714577C01", "num": 5},
    ]
    # transfer.cj_transfer_maker("CNFS03-BH", "CNFS02-BH", sku_info_list, ["KW-SJQ-01"])
