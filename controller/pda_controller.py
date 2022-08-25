from config.api_config.wms_api import wms_api_config
from config.sys_config import env_config
from tools.request_operator import RequestOperator
from controller.ums_controller import UmsController
from controller.wms_controller import WmsController

class PdaController(RequestOperator):

    def __init__(self, ums):
        self.prefix = env_config.get("app_prefix")
        self.headers = ums.header
        self.wms = WmsController(ums)
        super().__init__(self.prefix, self.headers)

    def pda_picking_detail(self, pick_order_no):
        """
        pda-获取拣货单信息
        :param pick_order_no:
        :return:
        """
        wms_api_config.get("pda_picking_detail")["data"].update({
            "pickOrderNo": pick_order_no
        })
        try:
            res = self.send_request(**wms_api_config.get("pda_picking_detail"))
            print("拣货单详情：", res)
            return res
        except Exception as e:
            raise Exception("err_info:", e)

    def pda_submit_tray_info(self, location_code_list, picking_detail_info):
        """
        按需装托
        :param location_code_list: 装托需要的托盘（当前仅支持一个托盘装托）
        :param picking_detail_info: 拣货单信息，可通过pda_picking_detail()方法获取
        :return:
        """
        if picking_detail_info:
            pick_order_no = picking_detail_info.get("pickOrderNo")
            tray_infos = []     # 装托的sku信息
            data = []       # 接口内参数信息
            # 通过获取拣货单内已拣货sku信息列表数据，拼接按需装托相关参数
            for i in picking_detail_info.get("details"):
                sku_info = {
                    "id": i["id"],
                    "waresSkuCode": i["waresSkuCode"],
                    "waresSkuName": i["waresSkuName"],
                    "goodsSkuCode": i["goodsSkuCode"],
                    "goodsSkuName": i["goodsSkuName"],
                    "skuQty": i["realPickQty"]
                }
                tray_infos.append(sku_info)
            item = {
                "storageLocationCode": location_code_list[0],
                "pickOrderNo": pick_order_no,
                "trayInfos": tray_infos
            }
            data.append(item)
            wms_api_config.get("pda_submit_tray_info")["data"] = data
            try:
                res = self.send_request(**wms_api_config.get("pda_submit_tray_info"))
                print("按需装托：", res)
                return res
            except Exception as e:
                raise Exception("err_info:", e)
        else:
            print("按需装托：传入的拣货单信息为空，请检查'pda_picking_detail()'函数返回参数")

    def pda_submit_tray_info_many(self, location_code_list, picking_detail_info):
        """
        按需装托
        :param location_code_list: 装托需要的托盘（当前仅支持一个托盘装托）
        :param picking_detail_info: 拣货单信息，可通过pda_picking_detail()方法获取
        :return:
        """
        if picking_detail_info:
            pick_order_no = picking_detail_info.get("pickOrderNo")
            tray_infos = []     # 装托的sku信息
            data = []       # 接口内参数信息
            # 通过获取拣货单内已拣货sku信息列表数据，拼接按需装托相关参数
            for i in picking_detail_info.get("details"):

                sku_info = {
                    "id": i["id"],
                    "waresSkuCode": i["waresSkuCode"],
                    "waresSkuName": i["waresSkuName"],
                    "goodsSkuCode": i["goodsSkuCode"],
                    "goodsSkuName": i["goodsSkuName"],
                    "skuQty": i["realPickQty"]
                }
                tray_infos.append(sku_info)

            item = {
                "storageLocationCode": location_code_list[0],
                "pickOrderNo": pick_order_no,
                "trayInfos": tray_infos
            }
            data.append(item)
            wms_api_config.get("pda_submit_tray_info")["data"] = data
            try:
                res = self.send_request(**wms_api_config.get("pda_submit_tray_info"))
                print("按需装托：", res)
                return res
            except Exception as e:
                raise Exception("err_info:", e)
        else:
            print("按需装托：传入的拣货单信息为空，请检查'pda_picking_detail()'函数返回参数")

    def pda_move_storage(self):
        """
        不成套移出
        :return:
        """
        pass

    def pda_finish_picking(self, pick_order_no, location_code):
        """
        创建调拨出库单
        @param pick_order_no:
        @param location_code:
        @return:
        """
        wms_api_config.get("pda_finish_picking")["data"].update({
            "pickOrderNo": pick_order_no,
            "storageLocationCodes": location_code
        })
        try:
            res = self.send_request(**wms_api_config.get("pda_finish_picking"))
            print("创建出库单结果：", res)  # 创建出库单结果： {'code': 200, 'message': '操作成功', 'data': 'DC2204120031'}
            return res
        except Exception as e:
            raise Exception("err_info:", e)


    def pda_review_submit(self, box_no, location_code):
        """
        调拨复核
        @param box_no:
        @param location_code_list:
        @return:
        """
        wms_api_config.get("pda_review_submit")["data"].update({
            "boxNo": box_no,
            "storageLocationCode": location_code
        })
        try:
            res = self.send_request(**wms_api_config.get("pda_review_submit"))
            print("调拨复核结果：", res)
            return res
        except Exception as e:
            raise Exception("err_info:", e)

    def pda_split_order(self):
        pass

    def pda_change_order(self):
        pass

    def pda_delete_order(self):
        pass

    def pda_handover_bind(self, box_no):
        """
        调拨发货-扫码箱单，生成交接单
        @param box_no:
        @return:
        """
        wms_api_config.get("pda_handover_bind")["data"].update({
            "boxNo": box_no,
        })
        try:
            res = self.send_request(**wms_api_config.get("pda_handover_bind"))
            print("调拨发货-扫码箱单，生成交接单：", res)
            return res
        except Exception as e:
            raise Exception("err_info:", e)

    def pda_delivery_confirm(self, hand_over_no):
        """
        调拨发货
        @return:
        """
        wms_api_config.get("pda_delivery_confirm")["data"].update({
            "handoverNo": hand_over_no,
        })
        try:
            res = self.send_request(**wms_api_config.get("pda_delivery_confirm"))
            print("调拨发货结果：", res)
            return res
        except Exception as e:
            raise Exception("err_info:", e)


    def pda_transfer_in_confirm(self, hand_over_no):
        """
        调拨入库-确认收货
        @param hand_over_no:
        @return:
        """
        wms_api_config.get("pda_transfer_in_confirm")["data"].update({
            "handoverNo": hand_over_no,
        })
        try:
            res = self.send_request(**wms_api_config.get("pda_transfer_in_confirm"))
            print("调拨入库-确认收货结果：", res)
            return res
        except Exception as e:
            raise Exception("err_info:", e)



    def pda_transfer_in_receive_all(self, box_no, storage_location_code, transfer_in_no):
        wms_api_config.get("pda_transfer_in_receive_all")["data"].update({
            "boxNo": box_no,
            "storageLocationCode": storage_location_code,
            "transferInNo": transfer_in_no
        })
        try:
            res = self.send_request(**wms_api_config.get("pda_transfer_in_receive_all"))
            print("调拨入库-整箱上架结果：", res)
            return res
        except Exception as e:
            raise Exception("err_info:", e)

    def pda_transfer_in_receive_one(self):
        pass



if __name__ == '__main__':
    ums = UmsController()
    pda = PdaController(ums)
    pda.wms.switch_warehouse("UKBH01")
    pick_order_no = "DJH2204140002"
    info = pda.pda_picking_detail(pick_order_no)

    picking_detail_info = info.get("data")
    location_code_list = ["KW-RQ-TP-01"]
    # location_code = "KW-RQ-TP-01"
    # 按需装托
    pda.pda_submit_tray_info(location_code_list, picking_detail_info)
    # 创建调拨出库单
    pda.pda_finish_picking(pick_order_no, location_code_list)

    # 获取调拨出库-箱单相关信息
    kw = {
        "transferOutNos": ['DC2204140002'],
    }
    res = pda.wms.search_box_out_list(**kw)
    out_box_no_list = res.get("data")["records"]
    # 调拨复核
    for i in out_box_no_list:
        pda.pda_review_submit(i.get("boxNo"), i.get("storageLocationCode"))
    # 调拨发货交接
    for i in out_box_no_list:
        res = pda.pda_handover_bind(i.get("boxNo"))
    # 调拨发货
    handover_no = res.get("data")["handoverNo"]
    # handover_no = "DBJJ2204120030"
    pda.pda_delivery_confirm(handover_no)


    # 调拨收货--整箱
    pda.pda_transfer_in_confirm(handover_no)
    kw_box_in = {
        "handoverNo": handover_no,
    }
    res = pda.wms.search_box_in_list(**kw_box_in)
    box_no_info = res.get("data")["records"]
    storage_location_code_list = ["KW-SJQ-01"]
    for i in box_no_info:
        pda.pda_transfer_in_receive_all(i.get("boxNo"), storage_location_code_list[0], i.get("transferInNo"))


    # box_no = "DC2204120030-1"
    # pda.pda_review_submit(box_no, location_code)
    # pda.pda_handover_bind(box_no)
    # handover_no = "DBJJ2204120030"
    # pda.pda_delivery_confirm(handover_no)




